import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
from pathlib import Path

# Step 1: Image processing functions
def process_image(image_path, size=(64, 64)):
    """Convert image to features"""
    try:
        img = Image.open(image_path).convert('L')  # Convert to grayscale
        img = img.resize(size)
        img_array = np.array(img).flatten()  # Convert to 1D array
        return img_array
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def collect_images_from_folder(folder_path, label):
    """Collect all images from a folder"""
    features = []
    labels = []
    
    if not os.path.exists(folder_path):
        return features, labels
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            img_path = os.path.join(folder_path, filename)
            feature = process_image(img_path)
            if feature is not None:
                features.append(feature)
                labels.append(label)
    
    return features, labels

# Step 2: Training function
def train_model(cat_folder, dog_folder):
    """Train the classifier"""
    print("Collecting cat images...")
    cat_features, cat_labels = collect_images_from_folder(cat_folder, 'cat')
    
    print("Collecting dog images...")
    dog_features, dog_labels = collect_images_from_folder(dog_folder, 'dog')
    
    if len(cat_features) == 0 or len(dog_features) == 0:
        print("Error: Need at least one image for each class")
        return None
    
    # Combine data
    X = cat_features + dog_features
    y = cat_labels + dog_labels
    
    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train SVM classifier
    print("Training model...")
    model = SVC(kernel='linear', probability=True)
    model.fit(X_train, y_train)
    
    # Test accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save model
    joblib.dump(model, 'cat_dog_classifier.pkl')
    print("Model saved as 'cat_dog_classifier.pkl'")
    
    return model, accuracy

# Step 3: Prediction function
def predict_image(model, image_path):
    """Predict if image is cat or dog"""
    feature = process_image(image_path)
    if feature is None:
        return "Error", 0
    
    feature = feature.reshape(1, -1)
    prediction = model.predict(feature)[0]
    probability = model.predict_proba(feature)[0]
    
    prob = probability[0] if prediction == 'cat' else probability[1]
    return prediction, prob

# Step 4: GUI Application
class CatDogClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat vs Dog Classifier")
        self.root.geometry("600x500")
        
        # Variables
        self.cat_folder = ""
        self.dog_folder = ""
        self.model = None
        self.accuracy = 0
        
        # Create GUI
        self.create_widgets()
        
        # Load model if exists
        if os.path.exists('cat_dog_classifier.pkl'):
            self.model = joblib.load('cat_dog_classifier.pkl')
            self.status_label.config(text="Model loaded successfully!")
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🐱 Cat vs Dog Classifier 🐶",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Training Section
        training_frame = tk.LabelFrame(self.root, text="Training", padx=10, pady=10)
        training_frame.pack(padx=10, pady=5, fill="x")
        
        # Cat Images
        cat_frame = tk.Frame(training_frame)
        cat_frame.pack(fill="x", pady=5)
        
        tk.Label(cat_frame, text="Cat Images Folder:").pack(side="left", padx=5)
        self.cat_entry = tk.Entry(cat_frame, width=40)
        self.cat_entry.pack(side="left", padx=5)
        
        tk.Button(
            cat_frame, 
            text="Browse", 
            command=lambda: self.browse_folder("cat")
        ).pack(side="left", padx=5)
        
        # Dog Images
        dog_frame = tk.Frame(training_frame)
        dog_frame.pack(fill="x", pady=5)
        
        tk.Label(dog_frame, text="Dog Images Folder:").pack(side="left", padx=5)
        self.dog_entry = tk.Entry(dog_frame, width=40)
        self.dog_entry.pack(side="left", padx=5)
        
        tk.Button(
            dog_frame, 
            text="Browse", 
            command=lambda: self.browse_folder("dog")
        ).pack(side="left", padx=5)
        
        # Train Button
        tk.Button(
            training_frame, 
            text="🚀 Train Model", 
            command=self.train_model_gui,
            bg="green", fg="white"
        ).pack(pady=10)
        
        # Testing Section
        test_frame = tk.LabelFrame(self.root, text="Testing", padx=10, pady=10)
        test_frame.pack(padx=10, pady=5, fill="x")
        
        # Test Image Selection
        test_image_frame = tk.Frame(test_frame)
        test_image_frame.pack(fill="x", pady=5)
        
        self.test_image_path = tk.StringVar()
        tk.Entry(test_image_frame, textvariable=self.test_image_path, width=40).pack(side="left", padx=5)
        
        tk.Button(
            test_image_frame, 
            text="Select Test Image", 
            command=self.select_test_image
        ).pack(side="left", padx=5)
        
        # Test Button
        tk.Button(
            test_frame, 
            text="🔍 Classify Image", 
            command=self.test_image,
            bg="blue", fg="white"
        ).pack(pady=10)
        
        # Result Display
        result_frame = tk.Frame(self.root)
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.result_text = tk.Text(result_frame, height=10, width=60)
        self.result_text.pack()
        
        # Status Bar
        self.status_label = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Instructions
        instructions = """
        Instructions:
        1. Create two folders: one for cat images, one for dog images
        2. Click 'Browse' to select each folder
        3. Click 'Train Model' to train the classifier
        4. Select any image and click 'Classify Image' to test
        5. Minimum 6 images each recommended for better accuracy
        """
        
        tk.Label(self.root, text=instructions, justify=tk.LEFT).pack(pady=10)
    
    def browse_folder(self, animal_type):
        folder = filedialog.askdirectory()
        if folder:
            if animal_type == "cat":
                self.cat_folder = folder
                self.cat_entry.delete(0, tk.END)
                self.cat_entry.insert(0, folder)
            else:
                self.dog_folder = folder
                self.dog_entry.delete(0, tk.END)
                self.dog_entry.insert(0, folder)
    
    def train_model_gui(self):
        if not self.cat_folder or not self.dog_folder:
            messagebox.showerror("Error", "Please select both cat and dog folders")
            return
        
        self.status_label.config(text="Training model... Please wait...")
        self.root.update()
        
        try:
            self.model, self.accuracy = train_model(self.cat_folder, self.dog_folder)
            
            if self.model:
                message = f"✅ Training Complete!\nAccuracy: {self.accuracy:.2%}"
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(1.0, message)
                self.status_label.config(text="Model trained successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")
            self.status_label.config(text="Training failed")
    
    def select_test_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.test_image_path.set(file_path)
    
    def test_image(self):
        if not self.model:
            messagebox.showerror("Error", "Please train the model first")
            return
        
        image_path = self.test_image_path.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image to test")
            return
        
        try:
            prediction, probability = predict_image(self.model, image_path)
            
            # Display image
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            
            # Create result message
            result = f"Image: {os.path.basename(image_path)}\n"
            result += f"Prediction: {prediction.upper()}\n"
            result += f"Confidence: {probability:.2%}\n\n"
            
            if prediction == 'cat':
                result += "🐱 यह एक बिल्ली है! (It's a Cat!)"
            else:
                result += "🐶 यह एक कुत्ता है! (It's a Dog!)"
            
            # Show in text box
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
            # Show image in new window
            self.show_image(img, prediction)
            
            self.status_label.config(text=f"Prediction: {prediction}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
    
    def show_image(self, img, prediction):
        # Create new window to display image
        img_window = tk.Toplevel(self.root)
        img_window.title(f"Prediction: {prediction}")
        
        # Convert PIL image to PhotoImage
        from PIL import ImageTk
        photo = ImageTk.PhotoImage(img)
        
        # Display image
        label = tk.Label(img_window, image=photo)
        label.image = photo  # Keep a reference
        label.pack()
        
        # Close button
        tk.Button(img_window, text="Close", command=img_window.destroy).pack(pady=5)

# Step 5: Simple Command Line Version (Alternative)
def simple_command_line_version():
    """Command line interface for quick testing"""
    print("=" * 50)
    print("Simple Cat vs Dog Classifier")
    print("=" * 50)
    
    # Ask for folders
    cat_folder = input("Enter path to cat images folder: ").strip()
    dog_folder = input("Enter path to dog images folder: ").strip()
    
    if not os.path.exists(cat_folder) or not os.path.exists(dog_folder):
        print("Error: Folders not found!")
        return
    
    # Train model
    print("\nTraining model...")
    model, accuracy = train_model(cat_folder, dog_folder)
    
    if model:
        print(f"\n✅ Model trained with {accuracy:.2%} accuracy")
        
        # Test loop
        while True:
            print("\n" + "=" * 30)
            test_image = input("\nEnter path to test image (or 'quit' to exit): ").strip()
            
            if test_image.lower() == 'quit':
                break
            
            if not os.path.exists(test_image):
                print("Error: Image not found!")
                continue
            
            prediction, prob = predict_image(model, test_image)
            
            print(f"\n🔍 Result:")
            print(f"Image: {os.path.basename(test_image)}")
            print(f"Prediction: {prediction}")
            print(f"Confidence: {prob:.2%}")
            
            if prediction == 'cat':
                print("🐱 यह एक बिल्ली है! (It's a Cat!)")
            else:
                print("🐶 यह एक कुत्ता है! (It's a Dog!)")
            
            # Show image
            try:
                img = Image.open(test_image)
                img.thumbnail((200, 200))
                plt.imshow(img)
                plt.title(f"Prediction: {prediction}")
                plt.axis('off')
                plt.show()
            except:
                pass

# Step 6: Quick Start Script (बिल्कुल सरल)
def quick_start():
    """सबसे सरल संस्करण - बस चलाओ और इमेज डालो"""
    import warnings
    warnings.filterwarnings('ignore')
    
    print("🐱🐶 Cat vs Dog Classifier - Quick Start 🐶🐱")
    print("-" * 40)
    
    # Step 1: Prepare folders
    print("\nStep 1: Create two folders on your desktop:")
    print("1. 'cats' - put cat images here")
    print("2. 'dogs' - put dog images here")
    print("\nPress Enter when ready...")
    input()
    
    # Check folders
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    cat_folder = os.path.join(desktop, "cats")
    dog_folder = os.path.join(desktop, "dogs")
    
    if not os.path.exists(cat_folder):
        os.makedirs(cat_folder)
        print(f"Created folder: {cat_folder}")
    
    if not os.path.exists(dog_folder):
        os.makedirs(dog_folder)
        print(f"Created folder: {dog_folder}")
    
    print("\n✅ Folders created!")
    print(f"Cat images folder: {cat_folder}")
    print(f"Dog images folder: {dog_folder}")
    
    # Step 2: Wait for images
    print("\n" + "=" * 40)
    print("Step 2: Add images to folders")
    print("Add at least 6 cat images to 'cats' folder")
    print("Add at least 6 dog images to 'dogs' folder")
    print("\nPress Enter when images are added...")
    input()
    
    # Check images
    cat_images = [f for f in os.listdir(cat_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    dog_images = [f for f in os.listdir(dog_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"\nFound {len(cat_images)} cat images")
    print(f"Found {len(dog_images)} dog images")
    
    if len(cat_images) < 3 or len(dog_images) < 3:
        print("⚠️ Warning: Need at least 3 images each for good results")
    
    # Step 3: Train
    print("\n" + "=" * 40)
    print("Step 3: Training model...")
    
    model, accuracy = train_model(cat_folder, dog_folder)
    
    if model:
        print(f"\n✅ Model ready! Accuracy: {accuracy:.2%}")
        
        # Step 4: Test
        print("\n" + "=" * 40)
        print("Step 4: Test the model")
        
        while True:
            print("\nOptions:")
            print("1. Test an image")
            print("2. Exit")
            
            choice = input("\nEnter choice (1 or 2): ").strip()
            
            if choice == '2':
                print("\nThank you for using Cat vs Dog Classifier! 🙏")
                break
            
            if choice == '1':
                test_image = input("\nEnter full path to image: ").strip()
                
                if not os.path.exists(test_image):
                    print("❌ Image not found!")
                    continue
                
                prediction, prob = predict_image(model, test_image)
                
                print(f"\n" + "=" * 30)
                print("🎯 RESULT:")
                print(f"Image: {os.path.basename(test_image)}")
                print(f"Prediction: {prediction.upper()}")
                print(f"Confidence: {prob:.2%}")
                
                if prediction == 'cat':
                    print("🐱 यह एक बिल्ली है!")
                    print("🐱 This is a CAT!")
                else:
                    print("🐶 यह एक कुत्ता है!")
                    print("🐶 This is a DOG!")
                
                # Show image
                try:
                    img = Image.open(test_image)
                    img.thumbnail((300, 300))
                    plt.figure(figsize=(5,5))
                    plt.imshow(img)
                    plt.title(f"Prediction: {prediction.upper()} ({prob:.2%})")
                    plt.axis('off')
                    plt.show()
                except:
                    pass
            else:
                print("❌ Invalid choice!")

# Step 7: Main function to choose interface
def main():
    print("Choose interface type:")
    print("1. GUI Interface (Recommended)")
    print("2. Command Line Interface")
    print("3. Quick Start (बिल्कुल सरल)")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        # Run GUI
        root = tk.Tk()
        app = CatDogClassifierApp(root)
        root.mainloop()
    
    elif choice == "2":
        # Run command line
        simple_command_line_version()
    
    elif choice == "3":
        # Run quick start
        quick_start()
    
    else:
        print("Invalid choice! Running GUI by default...")
        root = tk.Tk()
        app = CatDogClassifierApp(root)
        root.mainloop()

# Step 8: Installation requirements
def install_requirements():
    """Install required packages"""
    requirements = """
    Required packages:
    - numpy
    - scikit-learn
    - pillow
    - matplotlib
    - joblib
    
    Install with: pip install numpy scikit-learn pillow matplotlib joblib
    
    For GUI version also install:
    - tkinter (usually comes with Python)
    
    Optional for better performance:
    - opencv-python (for advanced image processing)
    """
    print(requirements)

# Step 9: Run the program
if __name__ == "__main__":
    print("=" * 60)
    print("🐱 CAT vs DOG IMAGE CLASSIFIER 🐶")
    print("=" * 60)
    print("\nA simple machine learning project to classify cats and dogs")
    
    # Show installation instructions
    print("\nFirst, make sure you have installed the required packages.")
    install_now = input("\nDo you want to see installation instructions? (y/n): ").lower()
    
    if install_now == 'y':
        install_requirements()
        input("\nPress Enter to continue after installing packages...")
    
    # Start the program
    main()