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
    echo "  • Mod folder support"
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
    echo "  2) Run Test Suite"
    echo "  3) Setup Environment Only (install dependencies)"
    echo "  4) Configuration Management"
    echo "  5) Show Configuration Status"
    echo "  6) Exit"
    echo ""
    print_colored $YELLOW "Please select an option (1-6): "
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
    echo "  2) Show Current Configuration Status"
    echo "  3) Edit Configuration File"
    echo "  4) Reset to Default Configuration"
    echo "  5) Back to Main Menu"
    echo ""
    print_colored $YELLOW "Please select an option (1-5): "
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
                show_config_status
                ;;
            3)
                edit_config_file
                ;;
            4)
                reset_to_default_config
                ;;
            5)
                return
                ;;
            *)
                print_colored $RED "Invalid option. Please select 1-5."
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
    
    # Check if create_config.py exists
    if [ ! -f "create_config.py" ]; then
        print_colored $RED "Error: create_config.py not found in current directory"
        return 1
    fi

    # Run the configuration creation script
    if python3 create_config.py; then
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
    
    # Show current configuration source using Python
    if [ -f "config_manager.py" ]; then
        print_colored $BLUE "Current Configuration Source:"
        python3 -c "
from config_manager import ConfigManager
try:
    cm = ConfigManager()
    print(f'  📁 Using: {cm.get_current_config_source()}')
    print(f'  📂 Events directory: {cm.get_final_events_path()}')
    print(f'  🎯 Using mod folder: {cm.should_use_mod_folder()}')
    if cm.should_use_mod_folder():
        print(f'  📁 Mod folder: {cm.get_target_mod_folder()}')
        print(f'  ⬆️  Parent directory: {cm.is_parent_mod_folder()}')
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
    print(f'  📁 Source: {cm.get_current_config_source()}')
    print(f'  📂 Events: {cm.get_final_events_path()}')
    if cm.should_use_mod_folder():
        print(f'  🎯 Mod folder: {cm.get_target_mod_folder()}')
except Exception as e:
    print(f'  ❌ Error: {e}')
"
        echo ""
    fi

    # Make main.py executable
    chmod +x main.py

    # Run the main program
    python3 main.py
    
    echo ""
    print_colored $GREEN "Main program execution completed."
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
            run_tests
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        3)
            setup_environment
            echo ""
            print_colored $YELLOW "Press Enter to return to menu..."
            read -r
            ;;
        4)
            manage_configuration
            ;;
        5)
            show_config_status
            ;;
        6)
            print_colored $GREEN "Goodbye!"
            exit 0
            ;;
        *)
            print_colored $RED "Invalid option. Please select 1-6."
            echo ""
            print_colored $YELLOW "Press Enter to continue..."
            read -r
            ;;
    esac
done 