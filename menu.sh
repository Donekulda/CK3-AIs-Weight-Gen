#!/bin/bash

# CK3 AI Weight Generator - Menu Script
# This script provides a console menu to choose between running the main program
# or the test suite.

set -e  # Exit on any error

# Show welcome message on first run
show_welcome() {
    clear
    print_colored $BLUE "🎮 CK3 AI Weight Generator"
    print_colored $BLUE "========================="
    echo ""
    print_colored $GREEN "Welcome to the CK3 AI Weight Generator!"
    echo ""
    print_colored $YELLOW "This tool helps you generate CK3 AI modifiers based on character traits."
    print_colored $YELLOW "It processes event files and replaces AI model references with proper CK3 triggers."
    echo ""
    print_colored $BLUE "Key Features:"
    echo "  • Unified trait-based AI system"
    echo "  • Automatic event file processing"
    echo "  • CK3 mod folder support (Steam Workshop & Paradox Mods)"
    echo "  • Mod discovery and management"
    echo "  • Configuration management"
    echo "  • Comprehensive testing"
    echo ""
    print_colored $YELLOW "Press Enter to continue to the main menu..."
    read -r
}

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_colored() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show the menu
show_menu() {
    clear
    print_colored $BLUE "CK3 AI Weight Generator - Main Menu"
    print_colored $BLUE "=================================="
    echo ""
    print_colored $GREEN "Available options:"
    echo ""
    echo "  1) Run CK3 AI Weight Generator (main program)"
    echo "  2) Run CK3 Parser (new unified parser)"
    echo "  3) CK3 Mod Manager (discover and manage mods)"
    echo "  4) Setup Configuration (interactive setup)"
    echo "  5) Run Test Suite"
    echo "  6) Setup Environment Only (install dependencies)"
    echo "  7) Configuration Management"
    echo "  8) Show Configuration Status"
    echo "  9) Exit"
    echo ""
    print_colored $YELLOW "Please select an option (1-9): "
}

# Function to setup environment
setup_environment() {
    print_colored $BLUE "Setting up CK3 AI Weight Generator environment..."
    echo ""

    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_colored $RED "Error: Python 3 is not installed or not in PATH"
        exit 1
    fi

    # Check if we're in the correct directory
    if [ ! -d "models" ]; then
        print_colored $RED "Error: Please run this script from the CK3-AIs-Weight-Gen directory"
        print_colored $RED "Expected directory: models/"
        exit 1
    fi

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_colored $YELLOW "Creating virtual environment..."
        python3 -m venv venv
        print_colored $GREEN "Virtual environment created successfully."
    else
        print_colored $GREEN "Virtual environment already exists."
    fi

    # Activate virtual environment
    print_colored $YELLOW "Activating virtual environment..."
    source venv/bin/activate

    # Upgrade pip
    print_colored $YELLOW "Upgrading pip..."
    pip install --upgrade pip

    # Install requirements
    print_colored $YELLOW "Installing Python dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_colored $GREEN "Dependencies installed successfully."
    else
        print_colored $YELLOW "Warning: requirements.txt not found, installing basic dependencies..."
        pip install pathlib typing-extensions
    fi

    print_colored $GREEN "Environment setup complete!"
    echo ""
}

# Function to show configuration submenu
show_config_menu() {
    clear
    print_colored $BLUE "Configuration Management"
    print_colored $BLUE "======================="
    echo ""
    print_colored $GREEN "Available options:"
    echo ""
    echo "  1) Create User Configuration (from default)"
    echo "  2) Setup from Mod Directory (parse descriptor.mod)"
    echo "  3) Show Current Configuration Status"
    echo "  4) Edit Configuration File"
    echo "  5) Reset to Default Configuration"
    echo "  6) Test Configuration System"
    echo "  7) Back to Main Menu"
    echo ""
    print_colored $YELLOW "Please select an option (1-7): "
}

# Function to manage configuration
manage_configuration() {
    while true; do
        show_config_menu
        read -r config_choice

        case $config_choice in
            1)
                create_user_config
                ;;
            2)
                setup_from_mod_directory
                ;;
            3)
                show_config_status
                ;;
            4)
                edit_config_file
                ;;
            5)
                reset_to_default_config
                ;;
            6)
                test_configuration_system
                ;;
            7)
                return
                ;;
            *)
                print_colored $RED "Invalid option. Please select 1-7."
                echo ""
                print_colored $YELLOW "Press Enter to continue..."
                read -r
                ;;
        esac
    done
}

# Function to create user configuration
create_user_config() {
    print_colored $BLUE "Creating User Configuration..."
    echo ""
    
    # Check if setup_config.py exists
    if [ ! -f "setup_config.py" ]; then
        print_colored $RED "Error: setup_config.py not found in current directory"
        return 1
    fi

    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Run the configuration creation script
    if python3 setup_config.py; then
        print_colored $GREEN "✅ User configuration created successfully!"
        echo ""
        print_colored $YELLOW "Next steps:"
        echo "  1. Edit config.json with your custom settings"
        echo "  2. Configure target paths (events, mod folders)"
        echo "  3. Run the main program"
    else
        print_colored $RED "❌ Failed to create user configuration"
    fi
    
    echo ""
    print_colored $YELLOW "Press Enter to continue..."
    read -r
}

# Function to setup from mod directory
setup_from_mod_directory() {
    print_colored $BLUE "Setup from Mod Directory"
    print_colored $BLUE "======================="
    echo ""
    
    print_colored $YELLOW "Enter the path to your CK3 mod directory:"
    print_colored $YELLOW "(or press Enter to browse current directory)"
    read -r mod_path
    
    if [ -z "$mod_path" ]; then
        # Show available directories in current location
        print_colored $BLUE "Available directories in current location:"
        echo ""
        for dir in */; do
            if [ -d "$dir" ]; then
                echo "  $dir"
            fi
        done
        echo ""
        print_colored $YELLOW "Enter mod directory name:"
        read -r mod_path
    fi
    
    if [ -d "$mod_path" ]; then
        print_colored $GREEN "Setting up configuration from: $mod_path"
        echo ""
        
        # Add src directory to Python path
        export PYTHONPATH="${PYTHONPATH}:$(pwd)"
        
        if python3 setup_config.py "$mod_path"; then
            print_colored $GREEN "✅ Configuration updated from mod directory!"
            echo ""
            print_colored $YELLOW "Mod information has been loaded into config.json"
        else
            print_colored $RED "❌ Failed to setup from mod directory"
        fi
    else
        print_colored $RED "❌ Directory not found: $mod_path"
    fi
    
    echo ""
    print_colored $YELLOW "Press Enter to continue..."
    read -r
}

# Function to test configuration system
test_configuration_system() {
    print_colored $BLUE "Testing Configuration System"
    print_colored $BLUE "==========================="
    echo ""
    
    if [ ! -f "tests/test_config.py" ]; then
        print_colored $RED "Error: test_config.py not found in tests directory"
        return 1
    fi
    
    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    print_colored $YELLOW "Running configuration system tests..."
    echo ""
    
    if python3 tests/test_config.py; then
        print_colored $GREEN "✅ All configuration tests passed!"
    else
        print_colored $RED "❌ Some configuration tests failed"
    fi
    
    echo ""
    print_colored $YELLOW "Press Enter to continue..."
    read -r
}

# Function to show configuration status
show_config_status() {
    print_colored $BLUE "Configuration Status"
    print_colored $BLUE "==================="
    echo ""
    
    # Check if config files exist
    if [ -f "config.json" ]; then
        print_colored $GREEN "✅ User configuration file exists: config.json"
    else
        print_colored $YELLOW "⚠️  User configuration file not found: config.json"
    fi
    
    if [ -f "config.default.json" ]; then
        print_colored $GREEN "✅ Default configuration file exists: config.default.json"
    else
        print_colored $RED "❌ Default configuration file not found: config.default.json"
    fi
    
    echo ""
    
    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Show current configuration source using Python
    if [ -f "src/config_manager.py" ]; then
        print_colored $BLUE "Current Configuration Source:"
        python3 -c "
from src.config_manager import ConfigManager
try:
    cm = ConfigManager()
    mod_config = cm.get_mod_config()
    print(f'  📁 Using: {cm.get_current_config_source()}')
    print(f'  🎮 Mod name: {mod_config.name}')
    print(f'  📂 Events directory: {cm.get_final_events_path()}')
    print(f'  🎯 Using mod folder: {cm.should_use_mod_folder()}')
    if cm.should_use_mod_folder():
        print(f'  📁 Mod folder: {cm.get_target_mod_folder()}')
        print(f'  ⬆️  Parent directory: {cm.is_parent_mod_folder()}')
    print(f'  🔍 Steam Workshop: {cm.get_steam_workshop_path()}')
    print(f'  📦 Paradox Mods: {cm.get_paradox_mod_path()}')
except Exception as e:
    print(f'  ❌ Error reading configuration: {e}')
"
    fi
    
    echo ""
    print_colored $YELLOW "Press Enter to continue..."
    read -r
}

# Function to edit configuration file
edit_config_file() {
    print_colored $BLUE "Edit Configuration File"
    print_colored $BLUE "======================"
    echo ""
    
    if [ ! -f "config.json" ]; then
        print_colored $YELLOW "No user configuration file found. Creating one first..."
        create_user_config
        if [ ! -f "config.json" ]; then
            return
        fi
    fi
    
    print_colored $GREEN "Opening config.json for editing..."
    echo ""
    print_colored $YELLOW "Available editors:"
    echo "  1) nano (simple terminal editor)"
    echo "  2) vim (advanced terminal editor)"
    echo "  3) gedit (graphical editor - if available)"
    echo "  4) Custom editor"
    echo ""
    print_colored $YELLOW "Please select an editor (1-4): "
    read -r editor_choice
    
    case $editor_choice in
        1)
            if command -v nano &> /dev/null; then
                nano config.json
            else
                print_colored $RED "nano not found. Please install nano or choose another editor."
            fi
            ;;
        2)
            if command -v vim &> /dev/null; then
                vim config.json
            else
                print_colored $RED "vim not found. Please install vim or choose another editor."
            fi
            ;;
        3)
            if command -v gedit &> /dev/null; then
                gedit config.json &
            else
                print_colored $RED "gedit not found. Please install gedit or choose another editor."
            fi
            ;;
        4)
            print_colored $YELLOW "Enter custom editor command: "
            read -r custom_editor
            if command -v "$custom_editor" &> /dev/null; then
                "$custom_editor" config.json
            else
                print_colored $RED "Editor '$custom_editor' not found."
            fi
            ;;
        *)
            print_colored $RED "Invalid option."
            ;;
    esac
    
    echo ""
    print_colored $GREEN "Configuration file edited."
    print_colored $YELLOW "Press Enter to continue..."
    read -r
}

# Function to reset to default configuration
reset_to_default_config() {
    print_colored $BLUE "Reset to Default Configuration"
    print_colored $BLUE "============================="
    echo ""
    
    if [ -f "config.json" ]; then
        print_colored $YELLOW "Warning: This will delete your current user configuration file."
        print_colored $YELLOW "Are you sure you want to continue? (y/N): "
        read -r confirm
        
        if [[ $confirm =~ ^[Yy]$ ]]; then
            rm config.json
            print_colored $GREEN "✅ User configuration file deleted."
            print_colored $GREEN "Program will now use default configuration."
        else
            print_colored $YELLOW "Reset cancelled."
        fi
    else
        print_colored $YELLOW "No user configuration file found. Already using default configuration."
    fi
    
    echo ""
    print_colored $YELLOW "Press Enter to continue..."
    read -r
}

# Function to run main program
run_main_program() {
    print_colored $BLUE "Running CK3 AI Weight Generator..."
    echo ""
    
    # Check if main.py exists
    if [ ! -f "main.py" ]; then
        print_colored $RED "Error: main.py not found in current directory"
        return 1
    fi

    # Check configuration status
    print_colored $YELLOW "Checking configuration..."
    if [ ! -f "config.json" ]; then
        print_colored $YELLOW "⚠️  No user configuration found. Using default configuration."
        print_colored $YELLOW "   Consider creating a custom configuration for better control."
    else
        print_colored $GREEN "✅ User configuration found."
    fi
    
    echo ""
    
    # Show current configuration source
    if [ -f "config_manager.py" ]; then
        print_colored $BLUE "Current Configuration:"
        python3 -c "
from config_manager import ConfigManager
try:
    cm = ConfigManager()
    mod_config = cm.get_mod_config()
    print(f'  📁 Source: {cm.get_current_config_source()}')
    print(f'  🎮 Mod: {mod_config.name}')
    print(f'  📂 Events: {cm.get_final_events_path()}')
    if cm.should_use_mod_folder():
        print(f'  🎯 Mod folder: {cm.get_target_mod_folder()}')
except Exception as e:
    print(f'  ❌ Error: {e}')
"
        echo ""
    fi

    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Make main.py executable
    chmod +x main.py

    # Run the main program
    python3 main.py
    
    echo ""
    print_colored $GREEN "Main program execution completed."
}

# Function to run CK3 parser
run_ck3_parser() {
    print_colored $BLUE "Running CK3 Parser..."
    echo ""
    
    # Check if ck3_parser.py exists
    if [ ! -f "src/ck3_parser.py" ]; then
        print_colored $RED "Error: ck3_parser.py not found in src directory"
        return 1
    fi

    # Check configuration status
    print_colored $YELLOW "Checking configuration..."
    if [ ! -f "config.json" ]; then
        print_colored $YELLOW "⚠️  No user configuration found. Using default configuration."
    else
        print_colored $GREEN "✅ User configuration found."
    fi
    
    echo ""
    
    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Show current configuration source
    if [ -f "src/config_manager.py" ]; then
        print_colored $BLUE "Current Configuration:"
        python3 -c "
from src.config_manager import ConfigManager
try:
    cm = ConfigManager()
    mod_config = cm.get_mod_config()
    print(f'  📁 Source: {cm.get_current_config_source()}')
    print(f'  🎮 Mod: {mod_config.name}')
    print(f'  📂 Events: {cm.get_final_events_path()}')
    if cm.should_use_mod_folder():
        print(f'  🎯 Mod folder: {cm.get_target_mod_folder()}')
except Exception as e:
    print(f'  ❌ Error: {e}')
"
        echo ""
    fi

    # Make ck3_parser.py executable
    chmod +x src/ck3_parser.py

    # Run the CK3 parser
    python3 src/ck3_parser.py
    
    echo ""
    print_colored $GREEN "CK3 Parser execution completed."
}

# Function to run CK3 mod manager
run_ck3_mod_manager() {
    print_colored $BLUE "Running CK3 Mod Manager..."
    echo ""
    
    # Check if ck3_mod_manager.py exists
    if [ ! -f "src/ck3_mod_manager.py" ]; then
        print_colored $RED "Error: ck3_mod_manager.py not found in src directory"
        return 1
    fi

    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"

    print_colored $YELLOW "This will scan for CK3 mods in Steam Workshop and Paradox mods directories."
    print_colored $YELLOW "You can browse available mods and get configuration snippets."
    echo ""

    # Make ck3_mod_manager.py executable
    chmod +x src/ck3_mod_manager.py

    # Run the CK3 mod manager
    python3 src/ck3_mod_manager.py
    
    echo ""
    print_colored $GREEN "CK3 Mod Manager completed."
}

# Function to run setup configuration
run_setup_configuration() {
    print_colored $BLUE "Running Setup Configuration..."
    echo ""
    
    # Check if setup_config.py exists
    if [ ! -f "setup_config.py" ]; then
        print_colored $RED "Error: setup_config.py not found in current directory"
        return 1
    fi

    print_colored $YELLOW "This will help you set up your configuration interactively."
    print_colored $YELLOW "You can also set up from a mod directory to auto-detect settings."
    echo ""

    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Make setup_config.py executable
    chmod +x setup_config.py

    # Run the setup configuration
    python3 setup_config.py
    
    echo ""
    print_colored $GREEN "Setup Configuration completed."
}

# Function to run tests
run_tests() {
    print_colored $BLUE "Running Test Suite..."
    echo ""
    
    # Check if tests directory exists
    if [ ! -d "tests" ]; then
        print_colored $RED "Error: tests directory not found"
        return 1
    fi

    # Find all test files
    test_files=$(find tests -name "test_*.py" -type f)
    if [ -z "$test_files" ]; then
        print_colored $RED "Error: No test files found in tests directory"
        return 1
    fi

    # Add src directory to Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Run all test files
    total_tests=0
    passed_tests=0
    failed_tests=0

    for test_file in $test_files; do
        print_colored $YELLOW "Running $(basename "$test_file")..."
        echo "----------------------------------------"
        
        if python3 "$test_file"; then
            print_colored $GREEN "✅ $(basename "$test_file") passed"
            ((passed_tests++))
        else
            print_colored $RED "❌ $(basename "$test_file") failed"
            ((failed_tests++))
        fi
        
        ((total_tests++))
        echo ""
    done

    echo "Test Results Summary"
    echo "==================="
    echo "Total tests run: $total_tests"
    echo "Passed: $passed_tests"
    echo "Failed: $failed_tests"

    if [ $failed_tests -eq 0 ]; then
        print_colored $GREEN "🎉 All tests passed!"
    else
        print_colored $RED "⚠️  Some tests failed. Please check the output above."
    fi
}

# Main menu loop
show_welcome
while true; do
    show_menu
    read -r choice

    case $choice in
        1)
            setup_environment
            run_main_program
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        2)
            setup_environment
            run_ck3_parser
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        3)
            setup_environment
            run_ck3_mod_manager
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        4)
            setup_environment
            run_setup_configuration
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        5)
            setup_environment
            run_tests
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        6)
            setup_environment
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        7)
            manage_configuration
            ;;
        8)
            show_config_status
            ;;
        9)
            print_colored $GREEN "Goodbye!"
            exit 0
            ;;
        *)
            print_colored $RED "Invalid option. Please select 1-9."
            echo ""
            print_colored $YELLOW "Press Enter to continue..."
            read -r
            ;;
    esac
done 