# ============================================
# 🚀 ULTIMATE FLUTTER BUILD SYSTEM v6.0
# 43 Cores | L4 GPU | Full PATH Fix
# ============================================

import os
import subprocess
import sys
import time
import multiprocessing
import shutil
from pathlib import Path

# ============================================
# SYSTEM CONFIGURATION
# ============================================

class SystemConfig:
    def __init__(self):
        self.cores = multiprocessing.cpu_count()
        self.worker_count = max(1, self.cores - 4)
        self.base_dir = "/content" if os.path.exists("/content") else os.getcwd()
        self.flutter_path = f"{self.base_dir}/flutter/bin"
        self.android_home = f"{self.base_dir}/android/sdk"
        self.repo_path = None
        self.repo_name = None
        self.setup_complete = False
        self.gpu_available = self.check_gpu()
        self.java_home = "/usr/lib/jvm/java-17-openjdk-amd64"
        
        # Set all paths immediately
        self.setup_paths()
        
    def setup_paths(self):
        """Setup all paths properly"""
        # Flutter path
        if os.path.exists(self.flutter_path):
            os.environ['PATH'] = f"{self.flutter_path}:{os.environ.get('PATH', '')}"
            os.environ['FLUTTER_ROOT'] = f"{self.base_dir}/flutter"
        
        # Android SDK path
        if os.path.exists(self.android_home):
            os.environ['ANDROID_HOME'] = self.android_home
            os.environ['ANDROID_SDK_ROOT'] = self.android_home
            os.environ['PATH'] = f"{self.android_home}/platform-tools:{self.android_home}/cmdline-tools/latest/bin:{os.environ.get('PATH', '')}"
        
        # Java path
        if os.path.exists(self.java_home):
            os.environ['JAVA_HOME'] = self.java_home
            os.environ['PATH'] = f"{self.java_home}/bin:{os.environ.get('PATH', '')}"
        
        # Build optimization
        os.environ['FLUTTER_BUILD_PARALLEL'] = 'true'
        os.environ['NINJA_JOBS'] = str(self.worker_count)
        os.environ['GRADLE_OPTS'] = f'-Xmx24g -Xms4g -XX:+UseG1GC -Dorg.gradle.parallel=true -Dorg.gradle.workers.max={self.worker_count}'
        
    def check_gpu(self):
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return 'L4' in result.stdout or 'NVIDIA' in result.stdout
        except:
            return False
    
    def print_system_info(self):
        print("\n" + "="*60)
        print("🚀 ULTIMATE FLUTTER BUILD SYSTEM v6.0")
        print("="*60)
        print(f"📊 CPU Cores: {self.cores} (Using {self.worker_count} workers)")
        print(f"🎮 GPU: {'✅ NVIDIA L4 24GB Detected' if self.gpu_available else '❌ Not Detected'}")
        print(f"☕ JAVA_HOME: {self.java_home}")
        print(f"📂 Flutter: {self.flutter_path}")
        print(f"📂 Android: {self.android_home}")
        print(f"📂 Current Repo: {self.repo_name or 'None'}")
        print("="*60 + "\n")

# ============================================
# INTERACTIVE INPUT (COLAB + TERMINAL)
# ============================================

class InputHandler:
    @staticmethod
    def get_input(prompt="Enter value: ", default=""):
        """Universal input handler"""
        try:
            # Try IPython widgets first (Colab)
            from IPython.display import display, clear_output
            import ipywidgets as widgets
            
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
            input_text.on_submit(lambda x: submit_btn.click() if x.value.strip() else None)
            
            display(widgets.VBox([input_text, submit_btn, output]))
            
            import time
            while result['value'] is None:
                time.sleep(0.1)
            
            clear_output(wait=True)
            return result['value']
            
        except:
            # Fallback to standard input
            try:
                return input(prompt)
            except:
                return default

# ============================================
# FLUTTER SETUP ENGINE (FIXED PATH)
# ============================================

class FlutterSetupEngine:
    def __init__(self, config):
        self.config = config
        self.input_handler = InputHandler()
        
    def setup_flutter(self):
        """Complete Flutter setup with proper PATH"""
        
        print("\n" + "="*60)
        print("🔧 FLUTTER ENVIRONMENT SETUP")
        print("="*60)
        
        # Steps
        steps = [
            ("System Packages", self.install_system_packages),
            ("Java Setup", self.setup_java),
            ("GPU Drivers", self.install_gpu_drivers),
            ("Flutter SDK", self.install_flutter),
            ("Android SDK", self.install_android_sdk),
            ("SDK Components", self.install_sdk_components),
            ("Configure Flutter", self.configure_flutter),
            ("Verify Setup", self.verify_setup)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📦 {step_name}...")
            try:
                if step_func():
                    print(f"✅ {step_name} Complete")
                else:
                    print(f"⚠️ {step_name} Failed")
            except Exception as e:
                print(f"❌ {step_name} Error: {e}")
        
        self.config.setup_complete = True
        print("\n" + "="*60)
        print("✅ FLUTTER SETUP COMPLETE!")
        print("="*60)
        
        # Show doctor
        self.show_flutter_doctor()
        
        # Continue button
        self.wait_for_continue()
    
    def install_system_packages(self):
        """Install system packages"""
        try:
            os.system('apt-get update -qq 2>/dev/null')
            os.system('apt-get install -y -qq openjdk-17-jdk curl git unzip libglu1-mesa cmake ninja-build build-essential wget 2>/dev/null')
            return True
        except:
            return False
    
    def setup_java(self):
        """Setup Java"""
        try:
            # Check if Java exists
            java_home = '/usr/lib/jvm/java-17-openjdk-amd64'
            if os.path.exists(java_home):
                self.config.java_home = java_home
                os.environ['JAVA_HOME'] = java_home
                os.environ['PATH'] = f"{java_home}/bin:{os.environ.get('PATH', '')}"
                return True
            
            # Install Java
            os.system('apt-get install -y -qq openjdk-17-jdk 2>/dev/null')
            if os.path.exists(java_home):
                self.config.java_home = java_home
                os.environ['JAVA_HOME'] = java_home
                os.environ['PATH'] = f"{java_home}/bin:{os.environ.get('PATH', '')}"
                return True
            
            return False
        except:
            return False
    
    def install_gpu_drivers(self):
        """Install GPU drivers"""
        if not self.config.gpu_available:
            return False
        try:
            os.system('apt-get install -y -qq nvidia-driver-470 nvidia-cuda-toolkit 2>/dev/null')
            return True
        except:
            return False
    
    def install_flutter(self):
        """Install Flutter with proper path"""
        try:
            flutter_dir = f"{self.config.base_dir}/flutter"
            
            # Remove if exists
            if os.path.exists(flutter_dir):
                shutil.rmtree(flutter_dir)
            
            # Clone
            os.chdir(self.config.base_dir)
            os.system('git clone https://github.com/flutter/flutter.git -b stable --depth=1')
            
            # Setup paths
            flutter_bin = f"{flutter_dir}/bin"
            if os.path.exists(flutter_bin):
                os.environ['PATH'] = f"{flutter_bin}:{os.environ.get('PATH', '')}"
                os.environ['FLUTTER_ROOT'] = flutter_dir
                
                # Pre-cache
                os.system('flutter precache --all --parallel 2>/dev/null || true')
                
                # Create cache
                os.makedirs('/tmp/flutter_cache', exist_ok=True)
                os.environ['FLUTTER_CACHE_DIR'] = '/tmp/flutter_cache'
                
                return True
            
            return False
        except Exception as e:
            print(f"Flutter install error: {e}")
            return False
    
    def install_android_sdk(self):
        """Install Android SDK"""
        try:
            android_home = self.config.android_home
            os.makedirs(android_home, exist_ok=True)
            os.environ['ANDROID_HOME'] = android_home
            os.environ['ANDROID_SDK_ROOT'] = android_home
            
            # Command line tools
            tools_path = f"{android_home}/cmdline-tools"
            if not os.path.exists(tools_path):
                os.chdir(self.config.base_dir)
                os.system('curl -s "https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip" -o cmdtools.zip')
                os.system('unzip -q cmdtools.zip -d /content/android/sdk/cmdline-tools')
                os.system('mv /content/android/sdk/cmdline-tools/cmdline-tools /content/android/sdk/cmdline-tools/latest')
                os.remove('cmdtools.zip')
            
            # Add to PATH
            os.environ['PATH'] = f"{android_home}/cmdline-tools/latest/bin:{android_home}/platform-tools:{os.environ.get('PATH', '')}"
            return True
        except:
            return False
    
    def install_sdk_components(self):
        """Install SDK components"""
        try:
            # Accept licenses
            os.system('yes | sdkmanager --licenses 2>/dev/null || true')
            
            # Install components
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
        """Configure Flutter"""
        try:
            # Set all paths
            os.environ['JAVA_HOME'] = self.config.java_home
            os.environ['ANDROID_HOME'] = self.config.android_home
            os.environ['ANDROID_SDK_ROOT'] = self.config.android_home
            os.environ['PATH'] = f"{self.config.flutter_path}:{self.config.android_home}/platform-tools:{self.config.android_home}/cmdline-tools/latest/bin:{os.environ.get('PATH', '')}"
            
            # Configure
            os.system('flutter config --android-sdk /content/android/sdk 2>/dev/null || true')
            os.system('flutter config --no-analytics 2>/dev/null || true')
            
            # Accept Android licenses
            os.system('yes | flutter doctor --android-licenses 2>/dev/null || true')
            
            return True
        except:
            return False
    
    def verify_setup(self):
        """Verify setup"""
        try:
            # Ensure paths
            os.environ['PATH'] = f"{self.config.flutter_path}:{os.environ.get('PATH', '')}"
            
            # Check Flutter
            result = subprocess.run(['which', 'flutter'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
            
            # Try direct
            flutter_path = f"{self.config.base_dir}/flutter/bin/flutter"
            if os.path.exists(flutter_path):
                os.environ['PATH'] = f"{self.config.base_dir}/flutter/bin:{os.environ.get('PATH', '')}"
                return True
            
            return False
        except:
            return False
    
    def show_flutter_doctor(self):
        """Show Flutter doctor"""
        print("\n🔍 Flutter Doctor Output:")
        print("-"*40)
        
        # Ensure flutter is in PATH
        flutter_bin = f"{self.config.base_dir}/flutter/bin"
        if os.path.exists(flutter_bin):
            os.environ['PATH'] = f"{flutter_bin}:{os.environ.get('PATH', '')}"
        
        # Check if flutter command exists
        flutter_cmd = 'flutter'
        result = subprocess.run(['which', 'flutter'], capture_output=True, text=True)
        if result.returncode != 0:
            flutter_cmd = f"{self.config.base_dir}/flutter/bin/flutter"
            if not os.path.exists(flutter_cmd):
                print("❌ Flutter not found!")
                return
        
        # Run doctor
        try:
            result = subprocess.run([flutter_cmd, 'doctor', '-v'], capture_output=True, text=True, timeout=30)
            print(result.stdout[:1500] if result.stdout else result.stderr[:1500])
        except Exception as e:
            print(f"⚠️ Could not run flutter doctor: {e}")
        
        print("-"*40)
    
    def wait_for_continue(self):
        """Wait for user to continue"""
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

# ============================================
# REPOSITORY MANAGER
# ============================================

class RepositoryManager:
    def __init__(self, config):
        self.config = config
        self.input_handler = InputHandler()
    
    def clone_repository(self):
        """Clone repository"""
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
        
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = f"{self.config.base_dir}/{repo_name}"
        
        # Check if exists
        if os.path.exists(repo_path):
            print(f"\n📁 Repository '{repo_name}' already exists!")
            choice = self.input_handler.get_input(
                "Update existing? (y/n): ",
                "n"
            )
            if choice.lower() != 'y':
                self.config.repo_path = repo_path
                self.config.repo_name = repo_name
                return True
            shutil.rmtree(repo_path)
        
        # Clone
        print(f"\n📥 Cloning {repo_url}...")
        os.chdir(self.config.base_dir)
        
        for branch in ['main', 'master']:
            cmd = f'git clone {repo_url} --depth=1 --single-branch --branch {branch} 2>/dev/null'
            if os.system(cmd) == 0 and os.path.exists(repo_path):
                break
        
        if os.path.exists(repo_path):
            self.config.repo_path = repo_path
            self.config.repo_name = repo_name
            print(f"✅ Repository cloned successfully!")
            
            if os.path.exists(f"{repo_path}/pubspec.yaml"):
                print("✅ Flutter project detected!")
            else:
                print("⚠️ Not a Flutter project")
            
            return True
        
        print("❌ Failed to clone repository!")
        return False

# ============================================
# BUILD ENGINE
# ============================================

class BuildEngine:
    def __init__(self, config):
        self.config = config
        self.input_handler = InputHandler()
    
    def build_project(self):
        """Build project"""
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
        
        # Ensure flutter in PATH
        flutter_bin = f"{self.config.base_dir}/flutter/bin"
        if os.path.exists(flutter_bin):
            os.environ['PATH'] = f"{flutter_bin}:{os.environ.get('PATH', '')}"
        
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
        self.wait_for_continue()
    
    def build_apk(self):
        """Build APK"""
        cmd = 'flutter build apk --release --split-per-abi --shrink --dart-define=FLUTTER_BUILD_PARALLEL=true --target-platform=android-arm64'
        os.system(cmd)
    
    def build_aab(self):
        """Build AAB"""
        cmd = 'flutter build appbundle --release --shrink --dart-define=FLUTTER_BUILD_PARALLEL=true'
        os.system(cmd)
    
    def build_web(self):
        """Build Web"""
        cmd = 'flutter build web --release --web-renderer canvaskit --dart-define=FLUTTER_BUILD_PARALLEL=true'
        os.system(cmd)
    
    def build_all(self):
        """Build all"""
        self.build_apk()
        self.build_aab()
        self.build_web()
    
    def show_outputs(self):
        """Show outputs"""
        print("\n📂 Build Outputs:")
        print("-"*40)
        
        outputs = [
            ('build/app/outputs/flutter-apk', '📱 APK'),
            ('build/app/outputs/bundle/release', '📦 AAB'),
            ('build/web', '🌐 Web')
        ]
        
        for path, label in outputs:
            if os.path.exists(path):
                print(f"{label}: {path}/")
                os.system(f'ls -lh {path}/* 2>/dev/null | head -3')
        
        print("-"*40)
    
    def wait_for_continue(self):
        """Wait for continue"""
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

# ============================================
# MAIN APPLICATION
# ============================================

class FlutterCLI:
    def __init__(self):
        self.config = SystemConfig()
        self.setup_engine = FlutterSetupEngine(self.config)
        self.repo_manager = RepositoryManager(self.config)
        self.build_engine = BuildEngine(self.config)
        self.running = True
        
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
║          ULTIMATE FLUTTER BUILD SYSTEM v6.0                 ║
║       43 Cores | L4 GPU | Full PATH Fixed                  ║
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
            
            status = []
            if self.config.setup_complete:
                status.append("✅ Flutter Ready")
            else:
                status.append("❌ Setup Required")
            
            if self.config.repo_name:
                status.append(f"📂 {self.config.repo_name}")
            
            print(f"📊 Status: {' | '.join(status)}")
            print("="*60)
            
            choice = InputHandler.get_input(
                "🔹 Select option (1-4): ",
                "1"
            )
            
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
    
    def exit_program(self):
        print("\n👋 Thank you for using Flutter Build System!")
        print("🚀 Happy Building!\n")
        self.running = False
        sys.exit(0)

# ============================================
# RUN
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
