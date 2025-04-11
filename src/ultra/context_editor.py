import os
import sys
import subprocess
import pickle
import tempfile
import threading
import time


# Context manager wrapper that updates the pickle file on changes
class ContextObserver:
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

    def check_for_external_updates(self):
        """Check if the editor has modified the pickle file and update if needed."""
        try:
            with open(self.pickle_path, "rb") as f:
                new_context = pickle.load(f)
                
            # Check if the context has changed
            if new_context != self.context_manager.context:
                # Update the context_manager with the new data
                self.context_manager.context = new_context
                return True
        except Exception:
            pass
        return False


class ContextEditor:
    """Handles visualization for context display using PyQt."""
    
    # Keep track of active context observers to prevent garbage collection
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
            
            # Save initial context data
            with open(pickle_path, "wb") as f:
                pickle.dump(context_provider.context, f)
            
            # Create an observer for this context manager
            observer = ContextObserver(context_provider, pickle_path)
            
            # Store reference to prevent garbage collection
            ContextEditor._active_observers.append(observer)
            
            # Set up a timer to check for updates from the editor
            def check_updates_periodically():
                while True:
                    time.sleep(refresh_interval / 1000 * 2)  # Check half as often as the refresh rate
                    observer.check_for_external_updates()
            
            # Start the update checker in a background thread
            update_thread = threading.Thread(target=check_updates_periodically, daemon=True)
            update_thread.start()
            
            # Launch the context window script as a separate process
            context_window_script = os.path.join(os.path.dirname(__file__), "context_window.py")
            with open(os.devnull, 'w') as devnull:
                subprocess.Popen(
                    [sys.executable, context_window_script, 
                     "--pickle-path", pickle_path, 
                     "--refresh-interval", str(refresh_interval)],
                    stdout=devnull,
                    stderr=devnull,
                    start_new_session=True
                )
                
        except Exception as e:
            raise ImportError(f"Could not start PyQt Context Window Editor: {str(e)}")
