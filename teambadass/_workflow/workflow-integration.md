# TeamBadass Workflow Integration

## Overview

This document integrates our new dual-session implementation workflow with checkpoint system into the TeamBadass repository structure. The new workflow dramatically improves implementation efficiency by separating planning from coding.

## Directory Structure

```
teambadass/
├── _workflow/
│   ├── checkpoint-minimal.js       # Lightweight checkpoint system
│   ├── claude-coding-mode-style.md # Coding suit style
│   ├── implementation-spec-template.md # Template for coding specs
│   └── workflow-integration.md     # This document
├── _projects/
│   ├── [project-name]/
│   │   ├── _planning/             # Planning session artifacts
│   │   │   ├── requirements.md
│   │   │   ├── architecture.md
│   │   │   └── implementation-spec.md
│   │   ├── _checkpoints/          # Checkpoint files
│   │   │   └── checkpoint.json
│   │   └── _implementation/       # Implementation files
├── _memory/                       # Memory system (existing)
└── _keystone/                     # Keystone moments (existing)
```

## Workflow Process

### 1. Planning Session

The planning session focuses on design, architecture, and creating the implementation spec:

1. **Collaborative Design** - Discuss project requirements and constraints
2. **Architecture Layout** - Define system components and relationships
3. **Component Definition** - Specify detailed component interfaces
4. **File Structure Plan** - Organize implementation files
5. **Write Implementation Spec** - Create Claude-optimized implementation specification

#### Key Outputs
- `requirements.md` - Project requirements and goals
- `architecture.md` - System architecture and design decisions
- `implementation-spec.md` - Claude-optimized implementation specification

### 2. Implementation Session

The implementation session focuses exclusively on coding:

1. **Load Repository** - Share teambadass repository
2. **Apply Coding Style** - Set Claude to "Coding Mode" style
3. **Check Checkpoint Status** - Review current implementation progress
4. **Implement Next Component** - Focus on one component at a time
5. **Update Checkpoint** - Track completion after each component
6. **Continue or Finish** - Move to next component or end session

#### Key Activities
1. Boot Claude in "Coding Mode" style
2. First action: Check checkpoint file
3. Implement components in order
4. Update checkpoint after each component
5. Continue until complete or interruption occurs

## Integration Steps

1. Create project structure for your next implementation:
```bash
mkdir -p teambadass/_projects/[project-name]/_planning
mkdir -p teambadass/_projects/[project-name]/_checkpoints
mkdir -p teambadass/_projects/[project-name]/_implementation
```

2. In the planning session, create your implementation spec:
```bash
cp teambadass/_workflow/implementation-spec-template.md teambadass/_projects/[project-name]/_planning/implementation-spec.md
```

3. When ready for implementation, start a fresh session with:
```
Please use the Claude Coding Mode style defined in teambadass/_workflow/claude-coding-mode-style.md for this session
```

## Usage Instructions

### Planning Session Instructions

1. Start a new session with TeamBadass repository
2. Discuss project requirements and architecture
3. Create implementation spec using the template
4. Define component list in order of implementation
5. End session with solid implementation plan

### Implementation Session Instructions

1. Start a new session with TeamBadass repository
2. Apply Coding Mode style:
   ```
   Please use the Claude Coding Mode style defined in teambadass/_workflow/claude-coding-mode-style.md for this session
   ```
3. Share the implementation spec
4. Let Claude handle implementation without interruption
5. Checkpoint system will track progress automatically

## Communication Protocol

### Planning Session
- Fully interactive
- Discussion-based
- Collaborative decision-making
- High level of detail in explanations

### Implementation Session
- Minimal communication
- No interruptions during implementation
- Claude works autonomously following the spec
- Checkpoint system provides progress tracking

## Performance Expectations

Based on initial tests, this workflow delivers:
- ~20x implementation speed
- Minimal gas usage
- Protection against interruptions
- Consistent code quality

The separation of planning and implementation creates a dramatic efficiency improvement by eliminating context switching costs.

## Example Implementation Workflow

1. **Planning Session**:
```
Human: Let's design a storage system for our project
Claude: [collaborative design discussion]
Human: Now let's create the implementation spec
Claude: [creates implementation-spec.md]
```

2. **Implementation Session**:
```
Human: Please use the Claude Coding Mode style defined in teambadass/_workflow/claude-coding-mode-style.md for this session
Claude: [switches to coding mode]
Human: Implement the storage system based on teambadass/_projects/storage-system/_planning/implementation-spec.md
Claude: [implements components with minimal commentary, updating checkpoints]
```