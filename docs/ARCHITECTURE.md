# 🏗️ System Architecture - OmniMaestro Guide System

> **Arquitectura del Sistema de Guía Inteligente**

---

## 📐 Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Interface                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Terminal   │  │  Git Hooks   │  │  Dashboard   │     │
│  │   Commands   │  │  (pre-commit)│  │    (MD)      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Core Guide System                          │
│                 (project_guide.py)                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            ProjectGuide Controller                    │  │
│  │  • Status Management                                  │  │
│  │  • Step Validation                                    │  │
│  │  • Dependency Checking                                │  │
│  │  • Platform Switching                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Command   │  │ Validation  │  │  Warnings   │        │
│  │   Router    │  │   Engine    │  │   System    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Steps     │  │    State     │  │   Roadmap    │     │
│  │ Definition   │  │   (.json)    │  │    (.md)     │     │
│  │  (STEPS)     │  └──────────────┘  └──────────────┘     │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flow de Comandos

### Status Command
```
User: python scripts/project_guide.py status
  │
  ▼
┌─────────────────────┐
│ Load State (.json)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Calculate Stats    │
│  • Progress %       │
│  • Next Step        │
│  • Warnings         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Display Output     │
│  (Colored Terminal) │
└─────────────────────┘
```

### Validate Command
```
User: python scripts/project_guide.py validate --step 5
  │
  ▼
┌─────────────────────┐
│ Check Dependencies  │
│   Are Complete?     │
└──────────┬──────────┘
           │
           ├─ No ──→ Error: Complete dependencies first
           │
           ▼ Yes
┌─────────────────────┐
│ Run Validation Cmds │
│  • Command 1        │
│  • Command 2        │
│  • Command 3        │
└──────────┬──────────┘
           │
           ├─ Failed ──→ Display Errors
           │
           ▼ Passed
┌─────────────────────┐
│ Mark as Completed   │
│ Update State        │
│ Update Dashboard    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Show Next Step      │
└─────────────────────┘
```

---

## 📊 Data Structure

### .project_state.json
```json
{
  "version": "1.0.0",
  "current_phase": "setup",
  "current_step": 5,
  "platform_target": "desktop",
  "completed_steps": [1, 2, 3, 4],
  "warnings": [
    {
      "type": "configuration",
      "severity": "high",
      "message": "...",
      "step_required": 5
    }
  ],
  "statistics": {
    "total_steps": 50,
    "completed_count": 4,
    "progress_percentage": 8
  }
}
```

### STEPS Dictionary (Python)
```python
STEPS = {
    1: {
        "name": "Step name",
        "phase": "setup|core_backend|desktop|mobile|web",
        "criticality": "critical|important|optional",
        "time_minutes": 60,
        "dependencies": [1, 2],
        "validation_commands": ["cmd1", "cmd2"],
        "resources": ["url1", "doc1"]
    }
}
```

---

## 🔌 Integration Points

### 1. Git Hooks Integration
```
Git Commit Trigger
    │
    ▼
.git/hooks/pre-commit
    │
    ├─ Validate Python syntax
    ├─ Check .env not committed
    ├─ Check file sizes
    │
    ▼
Call: python scripts/project_guide.py next
    │
    ▼
Show next recommended step
```

### 2. CI/CD Integration (Future)
```
GitHub Actions Trigger
    │
    ▼
Workflow: Validate Progress
    │
    ├─ Load .project_state.json
    ├─ Verify step completeness
    ├─ Run step validations
    │
    ▼
Update PR status
```

### 3. Evolution Log Integration
```
EVOLUTION_LOG.md
    │
    ▼
Detect new improvement
    │
    ▼
Check: Does it duplicate existing step?
    │
    ├─ Yes ──→ Warn user
    │
    ▼ No
Suggest when to implement
```

---

## 🎯 Component Responsibilities

### ProjectGuide Class
```python
class ProjectGuide:
    - Load/save state
    - Execute commands
    - Validate dependencies
    - Format output
    - Update dashboard
```

### Command Functions
```python
cmd_status()      # Display current status
cmd_next()        # Show next step details
cmd_validate()    # Run validation for step
cmd_roadmap()     # Display full roadmap
cmd_platform()    # Switch platform target
cmd_explain()     # Deep dive explanation
```

### Validation Engine
```python
_run_command()          # Execute shell command
_check_dependencies()   # Verify prerequisites
_mark_step_completed()  # Update state
```

---

## 🔐 Security Considerations

### Sensitive Data
- ✅ `.env` file excluded from commits (git hook check)
- ✅ API keys never logged or displayed
- ✅ State file doesn't contain secrets

### Command Execution
- ✅ Commands run with timeout (30s)
- ✅ Working directory restricted to project root
- ⚠️ Uses shell=True for complex commands (pipes, redirects)
- ✅ Commands are predefined in STEPS dictionary (not from user input)
- ✅ Safe in trusted development environments
- ⚠️ Do not modify STEPS with untrusted command strings

---

## 📈 Performance Characteristics

### Response Times
- `status`: < 100ms (read JSON + format)
- `next`: < 50ms (lookup + format)
- `validate`: 1-30s (depends on validation commands)
- `roadmap`: < 200ms (format all steps)

### Resource Usage
- Memory: < 50MB
- Disk: < 10KB (state file)
- CPU: Minimal (mostly I/O bound)

---

## 🚀 Extension Points

### Adding New Steps
```python
# In project_guide.py
STEPS[51] = {
    "name": "New step",
    "phase": "deployment",
    "criticality": "important",
    "time_minutes": 30,
    "dependencies": [50],
    "validation_commands": ["cmd"],
    "resources": ["url"]
}
```

### Adding New Commands
```python
def cmd_custom(self):
    """Custom command implementation"""
    # Your logic here
    pass

# In main()
if args.command == "custom":
    guide.cmd_custom()
```

### Custom Validations
```python
def _validate_custom(self, step_num: int) -> bool:
    """Custom validation logic"""
    # Your validation
    return True
```

---

## 🔮 Future Enhancements

### Planned Features
1. **Auto-detection of completed steps**
   - Scan filesystem for indicators
   - Check package.json/Cargo.toml dependencies
   - Verify Git history

2. **Interactive step completion**
   - Guided walkthrough in terminal
   - Step-by-step instructions
   - Real-time feedback

3. **Learning mode**
   - Track time taken per step
   - Predict completion times
   - Adjust estimates based on velocity

4. **Web Dashboard**
   - Visual progress tracking
   - Drag-and-drop step reordering
   - Team collaboration features

5. **AI Assistant Integration**
   - Explain steps with GPT-4
   - Debug validation failures
   - Suggest optimizations

---

## 📚 Related Documentation

- [PROJECT_ROADMAP.md](../PROJECT_ROADMAP.md) - Complete roadmap
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- Platform Guides: [Desktop](PLATFORM_GUIDES/DESKTOP_TAURI.md) | [Mobile](PLATFORM_GUIDES/MOBILE_FLUTTER.md) | [Web](PLATFORM_GUIDES/WEB_PWA.md)

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias  
**Versión:** 1.0.0
