import os
import sys
import subprocess
import pickle
import tempfile
import weakref

def create_viewer_script(context_data, pickle_path, refresh_interval):
    """Creates a temporary Python script that runs the PyQt viewer."""    
    # Save initial context data
    with open(pickle_path, "wb") as f:
        pickle.dump(context_data, f)
    
    script = f'''
import sys
import os
import pickle

# Suppress all output
os.environ['QT_LOGGING_RULES'] = '*.debug=false;*.warning=false'
os.environ['QT_LOGGING_TO_CONSOLE'] = '0'

from PyQt6 import QtWidgets, QtCore

class ContextWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Context View")
        self.pickle_path = "{pickle_path}"
        self.last_data_hash = None
        
        # Set up the text display
        self.text_widget = QtWidgets.QTextEdit()
        self.text_widget.setReadOnly(True)
        self.setCentralWidget(self.text_widget)
        self.resize(800, 600)
        
        # Set up the timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_text)
        self.timer.start({refresh_interval})
        
        self.update_text()
        self.show()
    
    def update_text(self):
        try:
            # Reload context from pickle file each time
            with open(self.pickle_path, "rb") as f:
                context_data = pickle.load(f)
            
            # Check if data changed to avoid unnecessary updates
            import hashlib
            data_hash = hashlib.md5(str(context_data).encode()).hexdigest()
            if self.last_data_hash == data_hash:
                return  # No changes, don't update
            self.last_data_hash = data_hash
            
            # Check if scrollbar is at the bottom before update
            scrollbar = self.text_widget.verticalScrollBar()
            was_at_bottom = scrollbar.value() >= scrollbar.maximum() - 20
                
            # Update the text content
            text = ""
            for msg in context_data:
                text += f"{{msg['role'].upper()}}: {{msg['content']}}\\n\\n"
            self.text_widget.setPlainText(text)
            
            # Only auto-scroll if we were already at the bottom
            if was_at_bottom:
                scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            print(f"Error updating text: {{e}}")

app = QtWidgets.QApplication([])
window = ContextWindow()
app.exec()
'''
    
    # Create a temporary file for the script
    fd, path = tempfile.mkstemp(suffix='.py', prefix='context_viewer_')
    with os.fdopen(fd, 'w') as f:
        f.write(script)
    return path


# Context manager wrapper that updates the pickle file on changes
class ContextManagerObserver:
    def __init__(self, context_manager, pickle_path):
        self.context_manager = context_manager
        self.pickle_path = pickle_path
        self.original_add_message = context_manager.add_message
        self.original_clear_context = context_manager.clear_context
        
        # Replace methods on this specific instance only
        context_manager.add_message = self.add_message
        context_manager.clear_context = self.clear_context
    
    def add_message(self, role, content):
        # Call original method first
        self.original_add_message(role, content)
        # Then update the pickle file
        self.update_pickle()
        
    def clear_context(self):
        # Call original method first
        self.original_clear_context()
        # Then update the pickle file
        self.update_pickle()
        
    def update_pickle(self):
        try:
            with open(self.pickle_path, "wb") as f:
                pickle.dump(self.context_manager.context, f)
        except Exception:
            pass  # Silently ignore errors


class ContextEditor:
    """Handles visualization for context display using PyQt."""
    
    # Keep track of active observers to prevent garbage collection
    _active_observers = []
    
    @staticmethod
    def start_gui_view(context_provider, refresh_interval=1000):
        """
        Launch a GUI window showing context that updates automatically.
        
        Args:
            context_provider: Object with a 'context' attribute that will be monitored
            refresh_interval: How often to refresh the view (in ms)
        """
        try:
            # Create a persistent pickle file path
            pickle_path = f"{tempfile.gettempdir()}/context_data_{id(context_provider)}.pickle"
            
            # Create the viewer script
            script_path = create_viewer_script(context_provider.context, pickle_path, refresh_interval)
            
            # Create an observer for this context manager
            observer = ContextManagerObserver(context_provider, pickle_path)
            
            # Store reference to prevent garbage collection
            ContextEditor._active_observers.append(observer)
            
            # Launch the script in a completely separate process
            with open(os.devnull, 'w') as devnull:
                subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=devnull,
                    stderr=devnull,
                    start_new_session=True
                )
                
        except Exception as e:
            raise ImportError(f"Could not start PyQt viewer: {str(e)}")
