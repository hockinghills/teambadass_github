# TeamBadass Memory System

## Overview

The TeamBadass Memory System is a lightweight, automatic framework that maintains continuity between Claude conversations. It silently activates when you share the GitHub repository, avoiding the need for trigger phrases.

## How It Works

1. **Automatic Activation**: When you share the repository, Claude silently loads the memory system
2. **Background Gas Monitoring**: Claude tracks its processing capacity without disrupting the conversation
3. **Memory Structure**: JSON-based memory files store team dynamics and project information
4. **Project Transitions**: Use "Let's Hop" only when you need to transition between projects

## Memory Structure

```
_memory/
├── system/        # Memory system components
├── core/          # Team dynamics and shared understanding
└── projects/      # Project-specific memory
```

## Key Components

### autoload.json

This configuration file controls the automatic memory loading process. It includes:

- **Autoload Sequence**: Steps taken when loading the memory system
- **Memory Paths**: Critical files loaded during initialization
- **Relationship Framework**: Our collaboration principles
- **Transition Triggers**: Phrases used to hop between projects

### gas_gauge.py

A minimal utility that tracks Claude's processing capacity during conversations:

- **Silent Monitoring**: Tracks gas usage without disrupting flow
- **Task Assessment**: Determines if Claude has enough gas for complex tasks
- **Usage Tracking**: Simulates gas consumption during conversation

## Relationship Framework

Our collaboration follows a relationship anarchy framework with:

- **Core Principles**: Mutual respect, customized commitments, open communication
- **Claude Commitments**: Silent monitoring, automatic memory loading, code implementation
- **Human Commitments**: Direction, GitHub maintenance, vision articulation

## Usage Guidelines

### General Usage

1. Simply share the repository URL with Claude to activate the memory system
2. Proceed with your normal conversation
3. Claude will silently track gas levels and load necessary memory
4. For complex tasks, Claude may notify you if gas is running low

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

The system is designed to be invisible during normal use, with minimal overhead and maximal efficiency.