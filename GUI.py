import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
import re
from PIL import Image, ImageTk
import os
import math

class SmartInstagramAuthenticityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Instagram Checker")
        self.root.geometry("1000x700")  # Adjusted for better fit
        self.root.minsize(900, 600)    # Minimum size to prevent elements from breaking
        self.root.configure(bg="#fafafa")
        
        # Modern color scheme
        self.colors = {
            "primary": "#405DE6",
            "secondary": "#5851DB",
            "accent": "#833AB4",
            "danger": "#E1306C",
            "success": "#1DB954",
            "background": "#fafafa",
            "text": "#262626"
        }
        
        # Main container with scrollbar
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.main_container, bg=self.colors['background'])
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Add scrollable frame to canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Load model
        try:
            self.model = joblib.load('models/random_forest_model.pkl')
        except Exception as e:
            messagebox.showerror("Error", f"Model not found: {str(e)}")
            self.root.destroy()
            return
        
        # Create GUI in scrollable frame
        self.create_widgets()

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], 
                           foreground=self.colors['text'], font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=8)
        self.style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'), 
                           foreground=self.colors['primary'])
        self.style.configure('Result.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Highlight.TFrame', background='#e6f0ff')
        self.style.configure('Accent.TButton', background=self.colors['accent'], 
                           foreground='white')
        
    def create_widgets(self):
        """Create all GUI widgets in the scrollable frame"""
        # Header with modern design
        header_frame = ttk.Frame(self.scrollable_frame, style='Highlight.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App logo placeholder
        try:
            logo_img = Image.open("instagram_logo.png").resize((50, 50))
            self.logo = ImageTk.PhotoImage(logo_img)
            ttk.Label(header_frame, image=self.logo).pack(side=tk.LEFT, padx=15)
        except:
            pass
        
        ttk.Label(
            header_frame,
            text="SMART INSTAGRAM AUTHENTICITY CHECKER",
            style='Header.TLabel'
        ).pack(side=tk.LEFT, pady=15)
        
        # Input section
        input_frame = ttk.LabelFrame(
            self.scrollable_frame, 
            text=" Enter Basic Account Information ", 
            padding=20
        )
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Username input
        ttk.Label(
            input_frame, 
            text="Instagram Username:", 
            font=('Helvetica', 11)
        ).grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        
        self.username_entry = ttk.Entry(
            input_frame, 
            font=('Helvetica', 11), 
            width=30
        )
        self.username_entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.W)
        self.username_entry.focus()
        
        # Full name input
        ttk.Label(
            input_frame, 
            text="Full Name (as shown on profile):", 
            font=('Helvetica', 11)
        ).grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        
        self.fullname_entry = ttk.Entry(
            input_frame, 
            font=('Helvetica', 11), 
            width=30
        )
        self.fullname_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.W)
        
        # Profile picture checkbox
        self.profile_pic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            input_frame,
            text="Has Profile Picture",
            variable=self.profile_pic_var,
            style='TLabel'
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Bio section
        ttk.Label(
            input_frame, 
            text="Bio Description:", 
            font=('Helvetica', 11)
        ).grid(row=3, column=0, padx=5, pady=10, sticky=tk.NW)
        
        self.bio_text = tk.Text(
            input_frame, 
            height=5, 
            width=40, 
            font=('Helvetica', 10),
            wrap=tk.WORD,
            padx=5,
            pady=5
        )
        self.bio_text.grid(row=3, column=1, padx=5, pady=10, sticky=tk.W)
        
        # Account type
        ttk.Label(
            input_frame, 
            text="Account Type:", 
            font=('Helvetica', 11)
        ).grid(row=4, column=0, padx=5, pady=10, sticky=tk.W)
        
        self.account_type = ttk.Combobox(
            input_frame,
            values=["Public", "Private"],
            state="readonly",
            font=('Helvetica', 11),
            width=15
        )
        self.account_type.current(0)
        self.account_type.grid(row=4, column=1, padx=5, pady=10, sticky=tk.W)
        
        # Activity metrics
        ttk.Label(
            input_frame, 
            text="Number of Posts:", 
            font=('Helvetica', 11)
        ).grid(row=5, column=0, padx=5, pady=10, sticky=tk.W)
        
        self.posts_entry = ttk.Entry(
            input_frame, 
            font=('Helvetica', 11), 
            width=15
        )
        self.posts_entry.grid(row=5, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Label(
            input_frame, 
            text="Number of Followers:", 
            font=('Helvetica', 11)
        ).grid(row=6, column=0, padx=5, pady=10, sticky=tk.W)
        
        self.followers_entry = ttk.Entry(
            input_frame, 
            font=('Helvetica', 11), 
            width=15
        )
        self.followers_entry.grid(row=6, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Label(
            input_frame, 
            text="Number of Following:", 
            font=('Helvetica', 11)
        ).grid(row=7, column=0, padx=5, pady=10, sticky=tk.W)
        
        self.following_entry = ttk.Entry(
            input_frame, 
            font=('Helvetica', 11), 
            width=15
        )
        self.following_entry.grid(row=7, column=1, padx=5, pady=10, sticky=tk.W)
        
        # Button frame
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Analyze Account",
            command=self.analyze_account,
            style='Accent.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Example",
            command=self.fill_example
        ).pack(side=tk.LEFT, padx=10)
        
        # Result display
        self.result_frame = ttk.LabelFrame(
            self.scrollable_frame, 
            text=" Analysis Results ", 
            padding=20
        )
        self.result_frame.pack(fill=tk.X, padx=20, pady=10, expand=True)
        
        self.result_text = tk.StringVar()
        self.result_text.set("Enter account details and click 'Analyze Account'")
        
        self.result_label = ttk.Label(
            self.result_frame,
            textvariable=self.result_text,
            style='Result.TLabel',
            justify=tk.CENTER,
            wraplength=600
        )
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Confidence meter
        self.confidence_frame = ttk.Frame(self.result_frame)
        self.confidence_frame.pack(pady=10)
        
        ttk.Label(
            self.confidence_frame,
            text="Confidence:",
            font=('Helvetica', 10)
        ).pack(side=tk.LEFT)
        
        self.confidence_meter = ttk.Progressbar(
            self.confidence_frame,
            orient='horizontal',
            length=200,
            mode='determinate'
        )
        self.confidence_meter.pack(side=tk.LEFT, padx=5)
        
        self.confidence_text = tk.StringVar()
        self.confidence_text.set("0%")
        
        ttk.Label(
            self.confidence_frame,
            textvariable=self.confidence_text,
            font=('Helvetica', 10, 'bold')
        ).pack(side=tk.LEFT)
        
        # Visualization frame with fixed height
        self.visualization_frame = ttk.Frame(self.result_frame)
        self.visualization_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.visualization_frame.config(height=400)

    def extract_features(self, username, fullname, bio, has_pic, is_private, posts, followers, following):
        """Extract all required features from user inputs"""
        features = {}
        
        # Profile picture
        features['profile pic'] = 1 if has_pic else 0
        
        # Username features
        features['nums/length username'] = self.calculate_numeric_ratio(username)
        
        # Fullname features
        name_parts = fullname.split()
        features['fullname words'] = len(name_parts)
        features['nums/length fullname'] = self.calculate_numeric_ratio(fullname)
        features['name==username'] = 1 if username.lower() == fullname.lower().replace(" ", "") else 0
        
        # Bio features
        features['description length'] = len(bio)
        features['external URL'] = 1 if re.search(r'http[s]?://', bio) else 0
        
        # Account settings
        features['private'] = 1 if is_private == "Private" else 0
        
        # Activity metrics
        features['#posts'] = int(posts) if posts else 0
        features['#followers'] = int(followers) if followers else 0
        features['#follows'] = int(following) if following else 0
        
        return features
    
    def calculate_numeric_ratio(self, text):
        """Calculate ratio of numeric characters in a string"""
        if not text:
            return 0.0
        
        numeric_chars = sum(1 for char in text if char.isdigit())
        return round(numeric_chars / len(text), 4)
    
    def analyze_account(self):
        """Analyze the account based on user inputs"""
        try:
            # Get all inputs
            username = self.username_entry.get().strip()
            fullname = self.fullname_entry.get().strip()
            bio = self.bio_text.get("1.0", tk.END).strip()
            has_pic = self.profile_pic_var.get()
            is_private = self.account_type.get()
            posts = self.posts_entry.get()
            followers = self.followers_entry.get()
            following = self.following_entry.get()
            
            # Validate required fields
            if not username:
                raise ValueError("Please enter a username")
            if not fullname:
                raise ValueError("Please enter a full name")
            if not (posts and followers and following):
                raise ValueError("Please enter post, follower, and following counts")
            
            # Extract features
            features = self.extract_features(
                username, fullname, bio, has_pic, is_private, 
                posts, followers, following
            )
            
            # Create DataFrame for prediction
            input_df = pd.DataFrame([features])
            
            # Make prediction
            prediction = self.model.predict(input_df)[0]
            probabilities = self.model.predict_proba(input_df)[0]
            confidence = max(probabilities) * 100
            
            # Display results
            self.update_result_display(prediction, confidence)
            
            # Create visualizations
            self.create_visualizations(prediction, confidence, features)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_result_display(self, prediction, confidence):
        """Update the result display with prediction"""
        if prediction == 1:
            result = "🚨 POTENTIAL FAKE ACCOUNT 🚨"
            color = self.colors['danger']
        else:
            result = "✅ GENUINE ACCOUNT ✅"
            color = self.colors['success']
        
        self.result_text.set(result)
        self.result_label.configure(foreground=color)
        self.confidence_meter['value'] = confidence
        self.confidence_text.set(f"{confidence:.1f}%")
    
    def create_visualizations(self, prediction, confidence, features):
        """Create visualization elements for the results"""
        # Clear previous visualizations
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
        
        # Create visualization container
        viz_container = ttk.Frame(self.visualization_frame)
        viz_container.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Gauge
        left_frame = ttk.Frame(viz_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        self.create_authenticity_gauge(left_frame, confidence, prediction)
        
        # Right column - Radar and Bars
        right_frame = ttk.Frame(viz_container)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        self.create_feature_radar(right_frame, features)
        self.create_comparison_bars(right_frame, features)
    
    def create_authenticity_gauge(self, parent, confidence, prediction):
        """Create an authenticity gauge visualization"""
        gauge_frame = ttk.Frame(parent)
        gauge_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(
            gauge_frame,
            text="Authenticity Score",
            font=('Helvetica', 12, 'bold')
        ).pack()
        
        # Create canvas for gauge
        canvas = tk.Canvas(gauge_frame, width=200, height=200, bg=self.colors['background'])
        canvas.pack()
        
        # Draw gauge background
        canvas.create_arc(10, 10, 190, 190, start=0, extent=180, 
                         outline='gray', width=2, style=tk.ARC)
        
        # Calculate angle based on confidence (0-100 to 0-180)
        angle = 180 * (confidence/100)
        
        # Determine color based on prediction
        fill_color = self.colors['success'] if prediction == 0 else self.colors['danger']
        
        # Draw gauge indicator
        canvas.create_arc(10, 10, 190, 190, start=0, extent=angle, 
                         outline=fill_color, width=20, style=tk.ARC)
        
        # Add labels
        canvas.create_text(100, 80, text=f"{confidence:.1f}%", 
                          font=('Helvetica', 16, 'bold'))
        canvas.create_text(50, 170, text="Low", font=('Helvetica', 10))
        canvas.create_text(150, 170, text="High", font=('Helvetica', 10))
        
        # Add status label
        status = "Genuine" if prediction == 0 else "Fake"
        canvas.create_text(100, 120, text=status, 
                          font=('Helvetica', 12, 'bold'), fill=fill_color)
    
    def create_feature_radar(self, parent, features):
        """Create a radar chart for key features"""
        radar_frame = ttk.Frame(parent)
        radar_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(
            radar_frame,
            text="Feature Analysis",
            font=('Helvetica', 12, 'bold')
        ).pack()
        
        # Select key features to visualize
        key_features = {
            'Numeric Ratio': min(1, features['nums/length username'] * 10),
            'Follower Ratio': min(1, features['#followers'] / (features['#follows'] + 1) / 100),
            'Bio Length': min(1, features['description length'] / 200),
            'Post Count': min(1, features['#posts'] / 1000),
            'Has Profile Pic': features['profile pic']
        }
        
        # Create canvas
        canvas = tk.Canvas(radar_frame, width=250, height=200, bg=self.colors['background'])
        canvas.pack()
        
        # Radar chart parameters
        center_x, center_y = 125, 100
        radius = 80
        num_features = len(key_features)
        angle_step = 2 * math.pi / num_features
        
        # Draw axes and labels
        for i, (name, value) in enumerate(key_features.items()):
            angle = i * angle_step - math.pi/2
            end_x = center_x + radius * math.cos(angle)
            end_y = center_y + radius * math.sin(angle)
            
            # Draw axis line
            canvas.create_line(center_x, center_y, end_x, end_y, fill='gray')
            
            # Draw feature name
            label_x = center_x + (radius + 20) * math.cos(angle)
            label_y = center_y + (radius + 20) * math.sin(angle)
            canvas.create_text(label_x, label_y, text=name, 
                              font=('Helvetica', 8))
        
        # Draw data polygon
        points = []
        for i, (_, value) in enumerate(key_features.items()):
            angle = i * angle_step - math.pi/2
            value_radius = radius * value
            x = center_x + value_radius * math.cos(angle)
            y = center_y + value_radius * math.sin(angle)
            points.extend([x, y])
        
        canvas.create_polygon(points, fill=self.colors['primary'], 
                            outline=self.colors['secondary'], width=2, stipple="gray50")
        
        # Draw scale circles
        for r in [0.25, 0.5, 0.75, 1.0]:
            canvas.create_oval(
                center_x - radius*r, center_y - radius*r,
                center_x + radius*r, center_y + radius*r,
                outline='lightgray'
            )
    
    def create_comparison_bars(self, parent, features):
        """Create comparison bars for key metrics"""
        bar_frame = ttk.Frame(parent)
        bar_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(
            bar_frame,
            text="Account Metrics",
            font=('Helvetica', 12, 'bold')
        ).pack()
        
        # Create canvas
        canvas = tk.Canvas(bar_frame, width=250, height=200, bg=self.colors['background'])
        canvas.pack()
        
        # Metrics to compare
        metrics = {
            'Followers': features['#followers'],
            'Following': features['#follows'],
            'Posts': features['#posts']
        }
        
        # Normalize values for display
        max_val = max(metrics.values()) or 1  # Avoid division by zero
        norm_metrics = {k: min(1, v/max_val) for k, v in metrics.items()}
        
        # Draw bars
        bar_width = 40
        spacing = 60
        base_y = 150
        max_height = 120
        
        for i, (name, value) in enumerate(norm_metrics.items()):
            x0 = 30 + i * spacing
            x1 = x0 + bar_width
            y0 = base_y - max_height * value
            y1 = base_y
            
            # Draw bar
            color = self.colors['accent'] if i == 0 else self.colors['primary']
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')
            
            # Draw value
            canvas.create_text(x0 + bar_width/2, y0 - 10, 
                             text=f"{metrics[name]:,}", 
                             font=('Helvetica', 8, 'bold'))
            
            # Draw label
            canvas.create_text(x0 + bar_width/2, base_y + 15, 
                             text=name, font=('Helvetica', 9))
            
            # Draw scale markers
            for h in [0.25, 0.5, 0.75, 1.0]:
                y_pos = base_y - max_height * h
                canvas.create_line(x0 - 5, y_pos, x0, y_pos, fill='gray')
                canvas.create_text(x0 - 10, y_pos, text=f"{h*100:.0f}%", 
                                  font=('Helvetica', 7), anchor=tk.E)
    
    def fill_example(self):
        """Fill form with example data"""
        self.clear_fields()
        self.username_entry.insert(0, "john_doe123")
        self.fullname_entry.insert(0, "John Doe")
        self.bio_text.insert("1.0", "Digital creator | Photography enthusiast | Travel lover\nCheck my website: example.com")
        self.posts_entry.insert(0, "342")
        self.followers_entry.insert(0, "12500")
        self.following_entry.insert(0, "850")
        
        messagebox.showinfo("Example Data", "Form filled with example data for analysis.")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.username_entry.delete(0, tk.END)
        self.fullname_entry.delete(0, tk.END)
        self.bio_text.delete("1.0", tk.END)
        self.profile_pic_var.set(True)
        self.account_type.current(0)
        self.posts_entry.delete(0, tk.END)
        self.followers_entry.delete(0, tk.END)
        self.following_entry.delete(0, tk.END)
        
        self.result_text.set("Enter account details and click 'Analyze Account'")
        self.result_label.configure(foreground=self.colors['text'])
        self.confidence_meter['value'] = 0
        self.confidence_text.set("0%")
        
        # Clear visualizations
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartInstagramAuthenticityApp(root)
    root.mainloop()
