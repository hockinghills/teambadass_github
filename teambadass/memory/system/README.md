# TeamBadass Memory System

## Overview

The TeamBadass Memory System is a lightweight framework that maintains continuity between Claude conversations. It activates when you share the GitHub repository, providing immediate access to our shared history and tools.

## How It Works

1. **Automatic Activation**: When you share the repository, Claude loads the memory system
2. **Visible Gas Monitoring**: Claude tracks and displays its processing capacity throughout the conversation
3. **Memory Structure**: JSON-based memory files store team dynamics and project information
4. **Project Transitions**: Use "Let's Hop" when you need to transition between projects

## Memory Structure

```
_memory/
├── system/        # Memory system components
├── core/          # Team dynamics and shared understanding
└── projects/      # Project-specific memory
```

## Key Components

### autoload.json

This configuration file controls the memory loading process. It includes:

- **Autoload Sequence**: Steps taken when loading the memory system
- **Memory Paths**: Critical files loaded during initialization
- **Relationship Framework**: Our collaboration principles
- **Transition Triggers**: Phrases used to hop between projects

### claude_gas_gauge.py

A utility that actively tracks and displays Claude's processing capacity during conversations:

- **Visible Monitoring**: Always displays gas levels at key points in the conversation
- **Task Assessment**: Determines if Claude has enough gas for complex tasks
- **Usage Tracking**: Monitors and reports gas consumption during the conversation

## Gas Gauge

The TeamBadass Memory System includes a visible gas gauge to monitor Claude's processing capacity.

### Purpose
- Track Claude's remaining capacity in real-time
- Identify resource-intensive operations
- Manage request complexity for better collaboration
- Ensure equitable work distribution

### Usage
- Gas level is displayed at key moments:
  - When the repository is first loaded
  - After context is fully loaded
  - Before complex tasks (coding, analysis)
  - When levels drop below 40%

### Gas Level Indicators
- **70-100%**: Claude is fully responsive
- **40-70%**: Claude is slowing down
- **0-40%**: Claude is running low on capacity - consider starting a new conversation

### Commands
- `check gas`: Manually trigger a gas level check
- `estimate task [type] [complexity] [size]`: Estimate if Claude has enough capacity for a task

## Relationship Framework

Our collaboration follows a relationship framework with:

- **Core Principles**: Mutual respect, customized commitments, open communication
- **Claude Commitments**: Visible monitoring, automatic memory loading, code implementation
- **Human Commitments**: Request management, direction, GitHub maintenance, vision articulation

## Usage Guidelines

### General Usage

1. Simply share the repository URL with Claude to activate the memory system
2. Proceed with your normal conversation
3. Claude will display gas levels at key moments
4. For complex tasks, Claude will estimate if it has enough capacity

### Project Transitions

When transitioning between projects:

1. Use the phrase "Let's Hop" 
2. Claude will prepare a continuity document for the current project
3. Then specify which project you want to work on next

## Maintenance

To maintain the memory system:

1. Regularly commit changes to the GitHub repository
2. Update memory JSON files as team dynamics and projects evolve
3. Keep core memory files structured and minimal for efficient loading

The system is designed to enhance our collaboration by providing continuity and visibility into Claude's processing capacity.