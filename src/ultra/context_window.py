import sys
import os
import pickle
import re
import time
import argparse

# Suppress Qt logging
os.environ['QT_LOGGING_RULES'] = '*.debug=false;*.warning=false'
os.environ['QT_LOGGING_TO_CONSOLE'] = '0'

from PyQt6 import QtWidgets, QtCore, QtGui

class ContextWindow(QtWidgets.QMainWindow):
    def __init__(self, pickle_path, refresh_interval):
        super().__init__()
        self.setWindowTitle("Live Context View (Editable)")
        self.pickle_path = pickle_path
        self.last_data_hash = None
        self.last_edit_time = 0
        self.is_updating = False
        self.dark_mode = False
        
        # Create a central widget with layout
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Set up the text display - now editable with rich text support
        self.text_widget = QtWidgets.QTextEdit()
        self.text_widget.setReadOnly(False)
        self.text_widget.textChanged.connect(self.on_text_edited)
        
        # Set a nice monospaced font for better readability of code blocks
        font = QtGui.QFont("Courier New", 10)
        self.text_widget.setFont(font)
        layout.addWidget(self.text_widget)
        
        # Create button row layout for controls
        button_layout = QtWidgets.QHBoxLayout()
        
        # Add save button
        save_button = QtWidgets.QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button)
        
        # Add a spacer to push buttons apart
        button_layout.addStretch()
        
        # Add a toggle for dark mode
        dark_mode_button = QtWidgets.QPushButton("Toggle Dark Mode")
        dark_mode_button.clicked.connect(self.toggle_dark_mode)
        button_layout.addWidget(dark_mode_button)
        
        # Add button row to main layout
        layout.addLayout(button_layout)
        
        self.setCentralWidget(central_widget)
        self.resize(800, 600)
        
        # Set up the timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_text)
        self.timer.start(refresh_interval)
        
        self.update_text()
        self.show()
    
    def on_text_edited(self):
        # Track when the last edit happened
        self.last_edit_time = time.time()
    
    def update_text(self):
        try:
            # Skip updates if user edited text in the last 2 seconds
            if time.time() - self.last_edit_time < 2:
                return
                
            # Avoid recursive updates
            if self.is_updating:
                return
                
            self.is_updating = True
            
            # Reload context from pickle file
            with open(self.pickle_path, "rb") as f:
                context_data = pickle.load(f)
            
            # Check if data changed to avoid unnecessary updates
            import hashlib
            data_hash = hashlib.md5(str(context_data).encode()).hexdigest()
            if self.last_data_hash == data_hash:
                self.is_updating = False
                return  # No changes, don't update
            self.last_data_hash = data_hash
            
            # Check if scrollbar is at the bottom before update
            scrollbar = self.text_widget.verticalScrollBar()
            was_at_bottom = scrollbar.value() >= scrollbar.maximum() - 20
                
            # Update the text content with rich text (HTML) formatting
            self.text_widget.clear()
            cursor = self.text_widget.textCursor()
            
            for msg in context_data:
                # Create a bold format for the role
                bold_format = QtGui.QTextCharFormat()
                bold_format.setFontWeight(QtGui.QFont.Weight.Bold)
                
                # Insert the role in bold
                cursor.insertText(msg["role"].upper() + ": ", bold_format)
                
                # Insert the content with normal formatting
                cursor.insertText(msg["content"] + "\n\n")
            
            # Ensure cursor is at the end
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
            
            # Only auto-scroll if we were already at the bottom
            if was_at_bottom:
                scrollbar.setValue(scrollbar.maximum())
                
            self.is_updating = False
        except Exception as e:
            self.is_updating = False
            print(f"Error updating text: {e}")

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Dark mode colors
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #2d2d2d; }
                QTextEdit { 
                    background-color: #2d2d2d; 
                    color: #e0e0e0; 
                    border: 1px solid #555555; 
                }
                QPushButton { 
                    background-color: #555555; 
                    color: #e0e0e0; 
                    border: 1px solid #777777;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover { background-color: #666666; }
            """)
        else:
            # Light mode (default)
            self.setStyleSheet("")
    
    def save_changes(self):
        try:
            # Parse text back into context format
            text = self.text_widget.toPlainText()
            
            # Simple parsing using regex pattern: "ROLE: content"
            pattern = r'(USER|ASSISTANT|SYSTEM):\s*(.*?)(?=\n\n[A-Z]+:|$)'
            matches = re.findall(pattern, text, re.DOTALL)
            
            new_context = []
            for role, content in matches:
                new_context.append({
                    'role': role.lower(),
                    'content': content.strip()
                })
            
            # Save back to pickle file
            with open(self.pickle_path, "wb") as f:
                pickle.dump(new_context, f)
                
            # Also create a backup file for safety
            backup_path = self.pickle_path + ".backup"
            with open(backup_path, "wb") as f:
                pickle.dump(new_context, f)
                
            # Reset the last edit time so we don't immediately override our change
            self.last_edit_time = time.time()
            
            QtWidgets.QMessageBox.information(self, "Save Successful", 
                                            "Your changes have been saved.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Save Failed", 
                                          f"Error saving changes: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Context Viewer')
    parser.add_argument('--pickle-path', required=True, help='Path to the pickle file')
    parser.add_argument('--refresh-interval', type=int, default=1000, help='Refresh interval in ms')
    args = parser.parse_args()
    
    app = QtWidgets.QApplication([])
    window = ContextWindow(args.pickle_path, args.refresh_interval)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()