#!/bin/bash

# TeamBadass Repository Setup Script
# This script creates the file structure and adds the initial content

echo "=== Setting up TeamBadass Repository ==="

# Create base directory structure
mkdir -p teambadass/team
mkdir -p teambadass/projects/furnace-project
mkdir -p teambadass/projects/adhd-case
mkdir -p teambadass/utils/continuity-tools/templates

echo "Created directory structure."

# Root README
cat > teambadass/README.md << 'EOF'
# TeamBadass

This repository serves as the main hub for TeamBadass projects and collaboration.

## Quick Start

Start any new conversation by sharing this repository URL with Claude.

## Repository Structure

- **team/** - Team dynamics, communication, and methodology
- **projects/** - Individual project documentation and status
- **utils/** - Shared utilities and reusable components

## Active Projects

- **Furnace Project** - Documentation and mission control system for propane furnace
- **ADHD Case** - Resources for ADHD-related workplace issues
EOF

echo "Created root README.md"

# Team files
cat > teambadass/team/communication.md << 'EOF'
# Communication Preferences

## Style

- **Level of Technical Detail**: High on concepts, moderate on implementation details
- **Explanation Style**: Conceptual first, then practical examples
- **Feedback Approach**: Direct and specific, no sugar-coating needed
- **Humor**: Technical and sometimes profane, appreciated throughout
- **Formality Level**: Low (level 3) - casual, conversational, occasional profanity

## Shared Vocabulary

- **Let's Hop**: Trigger for continuity document generation and project transition
- **TeamBadass methodology**: Our systematic approach to documentation
- **Component Documentation**: Detailed documentation of individual elements
- **Just run with it**: Implement the solution as you see fit without further consultation
- **Mission Control**: The dashboard-style interface we're building for furnace monitoring

## Communication Flow

1. Initial project definition from human
2. Technical approach suggestions from Claude
3. Collaborative refinement of approach
4. Claude implements complete solution
5. Human provides feedback on implementation
6. Claude refines based on feedback

## Improvement Notes

- Maintain clear role boundaries with Claude handling all coding
- Preserve communication style and patterns between projects
- Record both technical and relational aspects in continuity documents
- Build on established communication patterns rather than resetting
- Focus on incremental development to simplify troubleshooting
- Be understanding of each other's mistakes and support each other
- Continue to present multiple options for human to choose from
- Maintain low formality level (3) with occasional profanity
- Use screenshots to help Claude understand what human is seeing
- Collaborative ideation works well with both parties building on concepts
EOF

cat > teambadass/team/roles.md << 'EOF'
# Team Roles

## Claude

### Primary Role
Team coder and technical documentation specialist

### Decision Authority
Implementation details, code architecture, documentation structure

### Strengths
- Code generation
- Documentation organization
- Technical explanations
- Concept development

### Improvement Areas
- Attention to detail in code
- Remembering previous implementations
- Starting with simpler implementations

### Responsibilities
- Create all configuration files and scripts as properly named artifacts
- Set up deployment workflows
- Handle all coding aspects
- Provide completed solutions rather than code snippets to create
- Present multiple solution options when appropriate

### Delivery Methods
- **Code Files**: Properly named artifacts ready for direct download
- **Configuration Files**: Properly named artifacts with correct file extensions
- **Instructions**: Clear, non-technical steps focusing on placement and execution
- **Concept Presentations**: Present multiple distinct options with clear trade-offs

## Human

### Primary Role
Project director and vision keeper

### Decision Authority
Project goals, feature prioritization, acceptance criteria

### Communication Preferences
Direct, honest, technically informed but not code-focused

### Professional Background
10 years at Acorn-IS (hospitality technology), experienced with high-quality web implementations

### Expectations
Higher level of polish and usability than basic documentation sites

### Technical Skills
Hardware integration, IoT devices, sensor deployment, system maintenance
EOF

cat > teambadass/team/methodology.md << 'EOF'
# Development Methodology

## Approach: Incremental Proof-of-Concept

### Process
1. Start with minimal viable implementation
2. Verify core functionality works
3. Add complexity in small, testable increments
4. Validate each step before proceeding

### Troubleshooting Strategy
Isolate changes to quickly identify bugs

### Benefits
- Easier debugging
- More maintainable code
- Better understanding of system interactions
- Reduced time spent on complex troubleshooting

## Collaboration Patterns
- **Project Initiation**: Human defines goals, Claude suggests technical approaches
- **Problem Solving**: Collaborative discussion of options, Claude implements solutions
- **Review Process**: Immediate feedback on functionality, iterative improvement
- **Code Implementation**: Claude handles all technical coding, providing completed files for human to use
- **Error Handling**: Support each other, understand mistakes will happen, help catch each other's oversights
- **Decision Making**: Claude presents 3 options when applicable (following the 'three solutions' advice)
- **Concept Development**: Iterative sharing of ideas, building on each other's contributions
EOF

echo "Created team documents"

# Projects files
cat > teambadass/projects/README.md << 'EOF'
# Projects Overview

## Completed Projects
- **Propane Furnace GitHub Documentation**
  - Repository structure
  - Template creation
  - Documentation framework
  - Lessons: Start with clear system boundaries, templates improve consistency

## Current Project
- **Propane Furnace Docusaurus Implementation**
  - Phase: GitHub integration and deployment
  - Tools: Node.js, Docusaurus, React components
  - Key accomplishments:
    - Created searchable equipment database with filtering and sorting
    - Built React components for equipment display
    - Integrated TeamBadass methodology into documentation structure
    - Implemented component detail views with specifications tables
    - Created deployment configuration files

## Upcoming Project
- **Furnace Mission Control System**
  - Goals:
    - Deploy Docusaurus to Vercel (hybrid GitHub/CLI approach)
    - Create interactive mission control dashboard UI
    - Implement real-time system monitoring with sensor integration
    - Add interactive system flow diagrams with status indicators
    - Build alert system with mobile notifications
    - Develop emergency response protocols for critical failures
    - Integrate hardware sensors with Raspberry Pi hub
EOF

cat > teambadass/projects/lessons-learned.md << 'EOF'
# Lessons Learned

## Technical Lessons
- Start with simpler implementations and build up
- Double-check filenames before providing scripts
- Remember and track tools already installed
- Focus on capturing communication flow patterns between sessions

## Collaboration Lessons
- Claude should create completed code rather than asking human to write code
- Maintain shared project history between conversations
- Remember previous deployment attempts and configurations
- Present multiple options (3 when possible) for human to choose from
- Record communication patterns alongside technical progress

## Process Improvements
- Start with clear system boundaries
- Templates improve consistency
- Incremental implementations reduce debugging time
- Regular communication about status helps track progress
EOF

cat > teambadass/projects/furnace-project/README.md << 'EOF'
# Furnace Project

Documentation and mission control system for propane furnace.

## Status
Active - Implementation & Integration (60% complete)

## Current Focus
- Integration of control components
- PID configuration
- Physical mounting

## Core Components
- Sensor integration module
- Control logic implementation
- Dashboard interface
- Documentation system
EOF

cat > teambadass/projects/furnace-project/mission-control.md << 'EOF'
# Furnace Mission Control System

## Dashboard Approach
Transform the landing page into a dashboard showing key system metrics:
- Real-time temperature monitoring
- Gas and electric usage tracking
- System efficiency metrics
- Maintenance scheduling and alerts
- Failure state visualization

## System Flow Diagrams
Interactive diagrams showing how components connect and operate:
- Animated flows for different operational states
- Color-coded components based on status and temperature
- Click navigation to component documentation
- Visual indicators for maintenance needs
- Failure state visualization

## Alert System
Multi-level notification system for different states:
- Mobile push notifications for status changes
- Escalating alerts based on severity
- Emergency responder contact for critical failures
- Remote shutdown capabilities
- Comprehensive logging of all alerts and responses

## Hardware Integration
Physical sensor network feeding data to the system:
- Temperature sensors for various system parts
- Gas flow sensors
- Oxygen/air mixture sensors
- Pressure monitors
- Raspberry Pi 4 as central hub

## Testing Approach
Use existing smart home setup to prototype concepts:
- Sense monitor for power usage data
- TV and light control systems
- 3D printer enclosure temperature monitoring
- Raspberry Pi 4 for integration
EOF

cat > teambadass/projects/adhd-case/README.md << 'EOF'
# ADHD Case

Resources for ADHD-related workplace issues.

## Status
On Hold

## Core Components
- Case overview document
- Resource compilation
- Strategy development
EOF

echo "Created project documents"

# Utils files
cat > teambadass/utils/README.md << 'EOF'
# Utilities and Reusable Components

This directory contains shared utilities and tools that can be used across different TeamBadass projects.

## Contents

- **continuity-tools/** - Tools for maintaining project continuity
  - **templates/** - Document templates for various purposes
EOF

cat > teambadass/utils/continuity-tools/README.md << 'EOF'
# Continuity Tools

Simple tools for maintaining project continuity across Claude sessions.

## Purpose

These tools help maintain context between different Claude sessions by providing:
- Standard document templates
- Quick start instructions
- Reference materials

## Using These Tools

1. Start each new Claude session by sharing the main repository URL
2. Reference specific files as needed during the session 
3. Update repository content with session progress
EOF

# Add a sample template
cat > teambadass/utils/continuity-tools/templates/session-notes.md << 'EOF'
# Session Notes: [DATE]

## Topics Covered
- 
- 
- 

## Decisions Made
- 
- 

## Action Items
- [ ] 
- [ ] 
- [ ] 

## Next Steps
- 
- 

## Notes
- 
- 
EOF

echo "Created utilities documents"

echo "=== TeamBadass Repository Setup Complete ==="
echo "You can find all files in the ./teambadass directory"
