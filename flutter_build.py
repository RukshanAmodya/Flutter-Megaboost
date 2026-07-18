# ============================================
# 🚀 ULTIMATE FLUTTER BUILD SYSTEM v5.0
# Google Colab Optimized | 32 Cores | L4 GPU
# FIXED: JAVA_HOME | FIXED: Input Issues
# ============================================

import os
import subprocess
import sys
import time
import multiprocessing
import re
import shutil
from datetime import datetime

# ============================================
# SYSTEM CONFIGURATION
# ============================================

class SystemConfig:
    def __init__(self):
        self.cores = multiprocessing.cpu_count()
        self.worker_count = max(1, self.cores - 4)
        self.build_dir = "/content"
        self.repo_path = None
        self.repo_name = None
        self.setup_complete = False
        self.gpu_available = self.check_gpu()
        self.java_home = None
        
    def check_gpu(self):
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return 'L4' in result.stdout or 'NVIDIA' in result.stdout
        except:
            return False
    
    def setup_java_home(self):
        """Setup JAVA_HOME properly"""
        try:
            # Find Java installation
            java_paths = [
                '/usr/lib/jvm/java-17-openjdk-amd64',
                '/usr/lib/jvm/java-11-openjdk-amd64',
                '/usr/lib/jvm/default-java',
                '/usr/lib/jvm/java-8-openjdk-amd64'
            ]
            
            for path in java_paths:
                if os.path.exists(path):
                    self.java_home = path
                    os.environ['JAVA_HOME'] = path
                    os.environ['PATH'] += f":{path}/bin"
                    print(f"✅ JAVA_HOME set to: {path}")
                    return True
            
            # Try to find Java
            result = subprocess.run(['which', 'java'], capture_output=True, text=True)
            if result.returncode == 0:
                java_path = result.stdout.strip()
                java_home = os.path.dirname(os.path.dirname(java_path))
                if os.path.exists(java_home):
                    self.java_home = java_home
                    os.environ['JAVA_HOME'] = java_home
                    print(f"✅ JAVA_HOME set to: {java_home}")
                    return True
            
            # Install Java if not found
            print("📦 Installing Java...")
            os.system('apt-get update -qq && apt-get install -y -qq openjdk-17-jdk')
            os.system('update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java 2>/dev/null')
            
            # Set JAVA_HOME
            java_home = '/usr/lib/jvm/java-17-openjdk-amd64'
            if os.path.exists(java_home):
                self.java_home = java_home
                os.environ['JAVA_HOME'] = java_home
                os.environ['PATH'] += f":{java_home}/bin"
                print(f"✅ JAVA_HOME set to: {java_home}")
                return True
            
            return False
        except Exception as e:
            print(f"⚠️ Java setup error: {e}")
            return False
    
    def print_system_info(self):
        print("\n" + "="*60)
        print("🚀 ULTIMATE FLUTTER BUILD SYSTEM v5.0")
        print("="*60)
        print(f"📊 CPU Cores: {self.cores} (Using {self.worker_count} workers)")
        print(f"🎮 GPU: {'✅ NVIDIA L4 24GB Detected' if self.gpu_available else '❌ Not Detected'}")
        print(f"☕ JAVA_HOME: {self.java_home or 'Not Set'}")
        print(f"📂 Current Repo: {self.repo_name or 'None'}")
        print("="*60 + "\n")

# ============================================
# INTERACTIVE INPUT HANDLER (COLAB FRIENDLY)
# ============================================

class ColabInput:
    def __init__(self):
        self.input_value = None
        
    def get_input(self, prompt="Enter value: ", default=""):
        """Get user input in Colab using IPython widgets"""
        try:
            from IPython.display import display, clear_output
            import ipywidgets as widgets
            
            # Create widgets
            input_text = widgets.Text(
                description=prompt,
                placeholder='Type here...',
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='80%')
            )
            
            submit_btn = widgets.Button(
                description='✅ Submit',
                button_style='success',
                layout=widgets.Layout(width='auto')
            )
            
            output = widgets.Output()
            result = {'value': default}
            
            def on_submit(btn):
                with output:
                    clear_output()
                    value = input_text.value.strip()
                    if value:
                        result['value'] = value
                        print(f"✅ Received: {value}")
                    else:
                        print("❌ Please enter a value")
            
            submit_btn.on_click(on_submit)
            
            # Add Enter key support
            def on_enter(change):
                if change['type'] == 'change' and change['name'] == 'value':
                    if input_text.value.strip():
                        submit_btn.click()
            
            input_text.observe(on_enter)
            
            # Display
            container = widgets.VBox([input_text, submit_btn, output])
            display(container)
            
            # Wait for input
            import time
            while result['value'] is None:
                time.sleep(0.1)
            
            # Cleanup
            clear_output(wait=True)
            return result['value']
            
        except:
            # Fallback to simple input
            try:
                return input(prompt)
            except:
                print("⚠️ Input not available, using default")
                return default

# ============================================
# FLUTTER SETUP ENGINE (FIXED)
# ============================================

class FlutterSetupEngine:
    def __init__(self, config):
        self.config = config
        self.input_handler = ColabInput()
        
    def setup_flutter(self):
        """Setup Flutter with all fixes"""
        
        print("\n" + "="*60)
        print("🔧 FLUTTER ENVIRONMENT SETUP")
        print("="*60)
        
        # Step 0: Setup Java first
        print("\n☕ Setting up Java...")
        if not self.config.setup_java_home():
            print("❌ Failed to setup Java!")
            return
        
        # Steps
        steps = [
            ("System Packages", self.install_system_packages),
            ("GPU Drivers", self.install_gpu_drivers),
            ("Flutter SDK", self.install_flutter),
            ("Android SDK", self.install_android_sdk),
            ("SDK Components", self.install_sdk_components),
            ("Configure Flutter", self.configure_flutter),
            ("Verify Setup", self.verify_setup)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📦 {step_name}...")
            if step_func():
                print(f"✅ {step_name} Complete")
            else:
                print(f"⚠️ {step_name} Failed")
        
        self.config.setup_complete = True
        print("\n" + "="*60)
        print("✅ FLUTTER SETUP COMPLETE!")
        print("="*60)
        
        # Show doctor
        self.show_flutter_doctor()
        
        # Wait for user with IPython
        try:
            from IPython.display import display, clear_output
            import ipywidgets as widgets
            
            btn = widgets.Button(description='▶️ Continue to Main Menu', button_style='primary')
            display(btn)
            
            result = {'clicked': False}
            def on_click(b):
                result['clicked'] = True
            btn.on_click(on_click)
            
            while not result['clicked']:
                time.sleep(0.1)
            
            clear_output(wait=True)
        except:
            time.sleep(2)
            clear_output(wait=True)
    
    def install_system_packages(self):
        """Install required system packages"""
        try:
            os.system('apt-get update -qq 2>/dev/null')
            os.system('apt-get install -y -qq openjdk-17-jdk curl git unzip libglu1-mesa cmake ninja-build build-essential wget 2>/dev/null')
            return True
        except:
            return False
    
    def install_gpu_drivers(self):
        """Install NVIDIA GPU drivers"""
        if not self.config.gpu_available:
            return False
        try:
            os.system('apt-get install -y -qq nvidia-driver-470 nvidia-cuda-toolkit 2>/dev/null')
            return True
        except:
            return False
    
    def install_flutter(self):
        """Install Flutter SDK"""
        try:
            # Remove existing if corrupted
            if os.path.exists('/content/flutter'):
                shutil.rmtree('/content/flutter')
            
            os.system('git clone https://github.com/flutter/flutter.git -b stable --depth=1')
            os.environ['PATH'] += ":/content/flutter/bin"
            
            # Set Flutter environment
            os.environ['FLUTTER_ROOT'] = '/content/flutter'
            
            # Create cache
            os.makedirs('/tmp/flutter_cache', exist_ok=True)
            os.environ['FLUTTER_CACHE_DIR'] = '/tmp/flutter_cache'
            
            # Pre-cache
            os.system('flutter precache --all --parallel 2>/dev/null || true')
            
            return True
        except Exception as e:
            print(f"Flutter install error: {e}")
            return False
    
    def install_android_sdk(self):
        """Install Android SDK"""
        try:
            os.makedirs('/content/android/sdk', exist_ok=True)
            os.environ['ANDROID_HOME'] = "/content/android/sdk"
            os.environ['ANDROID_SDK_ROOT'] = "/content/android/sdk"
            
            # Command line tools
            tools_path = '/content/android/sdk/cmdline-tools'
            if not os.path.exists(tools_path):
                os.system('curl -s "https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip" -o cmdtools.zip')
                os.system('unzip -q cmdtools.zip -d /content/android/sdk/cmdline-tools')
                os.system('mv /content/android/sdk/cmdline-tools/cmdline-tools /content/android/sdk/cmdline-tools/latest')
                os.remove('cmdtools.zip')
            
            os.environ['PATH'] += ":/content/android/sdk/cmdline-tools/latest/bin:/content/android/sdk/platform-tools"
            return True
        except:
            return False
    
    def install_sdk_components(self):
        """Install SDK components with error handling"""
        try:
            # Accept licenses with proper redirect
            os.system('yes | sdkmanager --licenses 2>/dev/null || true')
            
            # Install components one by one to avoid errors
            components = [
                "platform-tools",
                "platforms;android-34",
                "build-tools;34.0.0"
            ]
            
            for comp in components:
                os.system(f'sdkmanager "{comp}" 2>/dev/null || true')
            
            return True
        except:
            return False
    
    def configure_flutter(self):
        """Configure Flutter settings"""
        try:
            # Set environment
            os.environ['JAVA_HOME'] = self.config.java_home or '/usr/lib/jvm/java-17-openjdk-amd64'
            os.environ['ANDROID_HOME'] = '/content/android/sdk'
            os.environ['ANDROID_SDK_ROOT'] = '/content/android/sdk'
            os.environ['PATH'] += ":/content/flutter/bin:/content/android/sdk/platform-tools"
            
            # Configure
            os.system('flutter config --android-sdk /content/android/sdk 2>/dev/null || true')
            os.system('flutter config --no-analytics 2>/dev/null || true')
            
            # Accept Android licenses
            os.system('yes | flutter doctor --android-licenses 2>/dev/null || true')
            
            # Set build optimizations
            os.environ['FLUTTER_BUILD_PARALLEL'] = 'true'
            os.environ['NINJA_JOBS'] = str(self.config.worker_count)
            
            return True
        except:
            return False
    
    def verify_setup(self):
        """Verify Flutter setup"""
        try:
            # Set PATH
            os.environ['PATH'] += ":/content/flutter/bin:/content/android/sdk/platform-tools"
            
            # Check Flutter
            result = subprocess.run(['flutter', 'doctor', '-v'], capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except:
            return False
    
    def show_flutter_doctor(self):
        """Display Flutter doctor output"""
        print("\n🔍 Flutter Doctor Output:")
        print("-"*40)
        
        # Set PATH
        os.environ['PATH'] += ":/content/flutter/bin:/content/android/sdk/platform-tools"
        
        # Run doctor
        result = subprocess.run(['flutter', 'doctor', '-v'], capture_output=True, text=True)
        print(result.stdout[:1000])  # First 1000 chars
        print("-"*40)

# ============================================
# REPOSITORY MANAGER
# ============================================

class RepositoryManager:
    def __init__(self, config):
        self.config = config
        self.input_handler = ColabInput()
    
    def clone_repository(self):
        """Clone GitHub repository"""
        
        print("\n" + "="*60)
        print("📥 CLONE REPOSITORY")
        print("="*60)
        
        print("\n📝 Enter GitHub Repository URL:")
        repo_url = self.input_handler.get_input(
            "Repository URL: ",
            "https://github.com/username/repo.git"
        )
        
        if not repo_url or repo_url == "https://github.com/username/repo.git":
            print("❌ Invalid repository URL!")
            return False
        
        # Extract repo name
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Check if exists
        if os.path.exists(f'/content/{repo_name}'):
            print(f"\n📁 Repository '{repo_name}' already exists!")
            choice = self.input_handler.get_input(
                "Update existing? (y/n): ",
                "n"
            )
            if choice.lower() != 'y':
                self.config.repo_path = f'/content/{repo_name}'
                self.config.repo_name = repo_name
                return True
        
        # Clone
        print(f"\n📥 Cloning {repo_url}...")
        os.chdir('/content')
        
        # Try different branches
        for branch in ['main', 'master']:
            cmd = f'git clone {repo_url} --depth=1 --single-branch --branch {branch}'
            result = os.system(cmd)
            if result == 0 and os.path.exists(f'/content/{repo_name}'):
                break
        
        if os.path.exists(f'/content/{repo_name}'):
            self.config.repo_path = f'/content/{repo_name}'
            self.config.repo_name = repo_name
            print(f"✅ Repository cloned successfully!")
            
            # Check if Flutter project
            if os.path.exists(f'/content/{repo_name}/pubspec.yaml'):
                print("✅ Flutter project detected!")
            else:
                print("⚠️ No pubspec.yaml found")
            
            return True
        else:
            print("❌ Failed to clone repository!")
            return False

# ============================================
# BUILD ENGINE
# ============================================

class BuildEngine:
    def __init__(self, config):
        self.config = config
        self.input_handler = ColabInput()
    
    def build_project(self):
        """Build Flutter project"""
        
        if not self.config.repo_path:
            print("\n❌ No repository loaded!")
            return
        
        if not self.config.setup_complete:
            print("\n⚠️ Flutter environment not setup!")
            return
        
        os.chdir(self.config.repo_path)
        
        print("\n" + "="*60)
        print("🏗️ BUILD REPOSITORY")
        print("="*60)
        print(f"📂 Building: {self.config.repo_name}")
        print("="*60)
        
        # Build options
        print("\n📱 Select Build Type:")
        print("1. 📱 Android APK (Release)")
        print("2. 📦 Android App Bundle (Release)")
        print("3. 🌐 Web (Release)")
        print("4. 🎯 All Platforms")
        print("5. 🔄 Back to Main Menu")
        
        choice = self.input_handler.get_input(
            "Select option (1-5): ",
            "1"
        )
        
        if choice == '5':
            return
        
        # Get dependencies
        print("\n📦 Fetching dependencies...")
        os.system('flutter pub get --parallel')
        
        # Build
        start_time = time.time()
        
        if choice == '1':
            self.build_apk()
        elif choice == '2':
            self.build_aab()
        elif choice == '3':
            self.build_web()
        elif choice == '4':
            self.build_all()
        
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        print("\n" + "="*60)
        print(f"⏱️ Build Time: {minutes}:{seconds:02d}")
        print("="*60)
        
        self.show_outputs()
        
        # Wait
        try:
            from IPython.display import display, clear_output
            import ipywidgets as widgets
            
            btn = widgets.Button(description='▶️ Continue', button_style='primary')
            display(btn)
            
            result = {'clicked': False}
            def on_click(b):
                result['clicked'] = True
            btn.on_click(on_click)
            
            while not result['clicked']:
                time.sleep(0.1)
            
            clear_output(wait=True)
        except:
            time.sleep(2)
            clear_output(wait=True)
    
    def build_apk(self):
        cmd = f'flutter build apk --release --split-per-abi --shrink --dart-define=FLUTTER_BUILD_PARALLEL=true --target-platform=android-arm64'
        os.system(cmd)
    
    def build_aab(self):
        cmd = f'flutter build appbundle --release --shrink --dart-define=FLUTTER_BUILD_PARALLEL=true'
        os.system(cmd)
    
    def build_web(self):
        cmd = f'flutter build web --release --web-renderer canvaskit --dart-define=FLUTTER_BUILD_PARALLEL=true'
        os.system(cmd)
    
    def build_all(self):
        self.build_apk()
        self.build_aab()
        self.build_web()
    
    def show_outputs(self):
        print("\n📂 Build Outputs:")
        print("-"*40)
        
        for path, label in [
            ('build/app/outputs/flutter-apk', '📱 APK'),
            ('build/app/outputs/bundle/release', '📦 AAB'),
            ('build/web', '🌐 Web')
        ]:
            if os.path.exists(path):
                print(f"{label}: {path}/")
                os.system(f'ls -lh {path}/* 2>/dev/null | head -3')
        
        print("-"*40)

# ============================================
# MAIN CLI APPLICATION
# ============================================

class FlutterCLI:
    def __init__(self):
        self.config = SystemConfig()
        self.setup_engine = FlutterSetupEngine(self.config)
        self.repo_manager = RepositoryManager(self.config)
        self.build_engine = BuildEngine(self.config)
        self.running = True
        
        # Clear and show banner
        from IPython.display import clear_output
        clear_output(wait=True)
        self.show_banner()
    
    def show_banner(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ███████╗██╗     ██╗   ██╗████████╗████████╗███████╗██████╗    ║
║     ██╔════╝██║     ██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗   ║
║     █████╗  ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝   ║
║     ██╔══╝  ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗   ║
║     ██║     ███████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║   ║
║     ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ║
║                                                              ║
║          ULTIMATE FLUTTER BUILD SYSTEM v5.0                 ║
║       Google Colab Optimized | 32 Cores | L4 GPU           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        self.config.print_system_info()
    
    def main_menu(self):
        from IPython.display import clear_output
        
        while self.running:
            print("\n" + "="*60)
            print("📱 MAIN MENU")
            print("="*60)
            print("1. 🔧 Setup Flutter Environment")
            print("2. 📥 Clone Repository")
            print("3. 🏗️ Build Repository")
            print("4. 🚪 Exit")
            print("="*60)
            
            # Status
            status = []
            if self.config.setup_complete:
                status.append("✅ Flutter Ready")
            else:
                status.append("❌ Setup Required")
            
            if self.config.repo_name:
                status.append(f"📂 {self.config.repo_name}")
            
            print(f"📊 Status: {' | '.join(status)}")
            print("="*60)
            
            choice = self.input_choice()
            
            if choice == '1':
                self.setup_engine.setup_flutter()
            elif choice == '2':
                self.repo_manager.clone_repository()
            elif choice == '3':
                self.build_engine.build_project()
            elif choice == '4':
                self.exit_program()
            else:
                print("❌ Invalid option!")
            
            clear_output(wait=True)
            self.show_banner()
    
    def input_choice(self):
        handler = ColabInput()
        return handler.get_input(
            "🔹 Select option (1-4): ",
            "1"
        )
    
    def exit_program(self):
        print("\n👋 Thank you for using Flutter Build System!")
        print("🚀 Happy Building!\n")
        self.running = False
        sys.exit(0)

# ============================================
# RUN THE APPLICATION
# ============================================

if __name__ == "__main__":
    try:
        app = FlutterCLI()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
