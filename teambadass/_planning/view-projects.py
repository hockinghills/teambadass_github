#!/usr/bin/env python3
"""
TeamBadass Project Viewer
Simple utility to view and filter projects from master-list.json
"""

import os
import json
import sys
import argparse
from datetime import datetime

# Base path for TeamBadass repository
BASE_PATH = "/home/louthenw/Documents/teambadass_github/teambadass"
MASTER_LIST_PATH = os.path.join(BASE_PATH, "_planning/master-list.json")

def load_master_list():
    """Load the master list from file"""
    try:
        with open(MASTER_LIST_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Master list not found at {MASTER_LIST_PATH}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Master list is not valid JSON")
        sys.exit(1)

def display_projects(projects, status_filter=None):
    """Display projects in a formatted table"""
    # Filter projects if status filter provided
    if status_filter:
        projects = [p for p in projects if p['status'] == status_filter]
    
    if not projects:
        print("No projects match the filter criteria")
        return
    
    # Print header
    print("\n{:<20} {:<25} {:<15} {:<10} {:<10}".format(
        "ID", "NAME", "STATUS", "COMPLETION", "PRIORITY"
    ))
    print("-" * 85)
    
    # Sort projects by status and priority
    status_order = {"implementing": 0, "planning": 1, "idea": 2, "completed": 3}
    priority_order = {"high": 0, "medium": 1, "low": 2}
    
    sorted_projects = sorted(projects, 
                             key=lambda p: (status_order.get(p.get('status', 'idea'), 99),
                                           priority_order.get(p.get('priority', 'medium'), 99),
                                           p.get('name', '')))
    
    # Print each project
    for project in sorted_projects:
        # Format status with emoji
        status_display = project.get('status', 'idea')
        status_emoji = {
            'idea': '💡',
            'planning': '🔍',
            'implementing': '🔨',
            'completed': '✅'
        }
        status = f"{status_emoji.get(status_display, '❓')} {status_display}"
        
        # Format priority with emoji
        priority_display = project.get('priority', 'medium')
        priority_emoji = {
            'high': '⚠️',
            'medium': '✦',
            'low': '•'
        }
        priority = f"{priority_emoji.get(priority_display, '•')} {priority_display}"
        
        print("{:<20} {:<25} {:<15} {:<10} {:<10}".format(
            project.get('id', ''),
            project.get('name', '')[:25],
            status,
            f"{project.get('completion', 0)}%",
            priority
        ))
    
    print()

def display_project_details(project_id, projects):
    """Display detailed information about a specific project"""
    # Find project
    project = next((p for p in projects if p.get('id') == project_id), None)
    
    if not project:
        print(f"Error: Project with ID '{project_id}' not found")
        return
    
    # Print project details
    print(f"\n📋 Project: {project.get('name')} ({project.get('id')})")
    print("-" * 80)
    print(f"Description: {project.get('description', 'No description')}")
    print(f"Status: {project.get('status', 'idea')}")
    print(f"Completion: {project.get('completion', 0)}%")
    print(f"Priority: {project.get('priority', 'medium')}")
    
    if 'path' in project:
        print(f"Path: {project.get('path')}")
    
    if 'created_at' in project:
        created_at = datetime.fromisoformat(project['created_at'])
        print(f"Created: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if 'completed_at' in project:
        completed_at = datetime.fromisoformat(project['completed_at'])
        print(f"Completed: {completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if 'next_steps' in project:
        print(f"\nNext Steps:")
        print(f"- {project['next_steps']}")
    
    print()

def main():
    """Main function"""
    # Parse arguments
    parser = argparse.ArgumentParser(description="TeamBadass Project Viewer")
    parser.add_argument('--status', choices=['idea', 'planning', 'implementing', 'completed'],
                        help='Filter projects by status')
    parser.add_argument('--info', metavar='PROJECT_ID',
                        help='Display detailed information about a specific project')
    args = parser.parse_args()
    
    # Load master list
    master_list = load_master_list()
    projects = master_list.get('projects', [])
    
    print(f"📂 TeamBadass Projects ({len(projects)} total)")
    print(f"Last updated: {master_list.get('updated', 'unknown')}")
    
    # Display project details if --info provided
    if args.info:
        display_project_details(args.info, projects)
    else:
        # Otherwise display all projects (optionally filtered)
        display_projects(projects, args.status)

if __name__ == "__main__":
    main()
