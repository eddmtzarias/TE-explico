# 📚 PixARR Design - API Documentation

## Core Modules

### PixARRAgent

Main autonomous agent for design artifact supervision.

#### Constructor

```python
PixARRAgent(workspace: Optional[str] = None)
```

**Parameters:**
- `workspace` (str, optional): Workspace path. Defaults to project root.

#### Methods

##### `activate() -> None`

Activate the agent and log the activation.

**Example:**
```python
agent = PixARRAgent()
agent.activate()
```

##### `create_artifact(file_path: str, creator: str) -> Dict[str, Any]`

Create and register a new design artifact.

**Parameters:**
- `file_path` (str): Path to the artifact file
- `creator` (str): Name of the creator

**Returns:**
- Dictionary containing artifact metadata

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `RuntimeError`: If agent is not activated

**Example:**
```python
metadata = agent.create_artifact("designs/active/logo.png", "Designer123")
print(metadata["hash"])  # SHA-256 hash
```

##### `modify_artifact(file_path: str, modifier: str, description: str) -> Dict[str, Any]`

Register a modification to an existing artifact.

**Parameters:**
- `file_path` (str): Path to the artifact file
- `modifier` (str): Name of the modifier
- `description` (str): Description of the modification

**Returns:**
- Dictionary containing updated artifact metadata

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `RuntimeError`: If agent is not activated

**Example:**
```python
metadata = agent.modify_artifact(
    "designs/active/logo.png",
    "Designer123",
    "Updated brand colors"
)
print(f"Version: {metadata['version']}")
```

##### `detect_unauthorized_access(file_path: str, suspicious_actor: str) -> None`

Detect and respond to unauthorized access attempts.

**Parameters:**
- `file_path` (str): Path to the compromised file
- `suspicious_actor` (str): Name of the suspicious actor

**Actions:**
- Moves file to quarantine
- Logs incident
- Sends HIGH severity alert

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `RuntimeError`: If agent is not activated

**Example:**
```python
agent.detect_unauthorized_access("designs/active/logo.png", "UnknownUser")
```

##### `audit_integrity(directory: Optional[str] = None) -> Dict[str, Any]`

Perform an integrity audit on all monitored files.

**Parameters:**
- `directory` (str, optional): Directory to audit. Defaults to active directory.

**Returns:**
- Dictionary with keys:
  - `summary`: Statistics about the audit
  - `results`: List of validation results
  - `anomalies`: List of files with integrity issues

**Example:**
```python
results = agent.audit_integrity()
print(f"Files verified: {results['summary']['total_files']}")
print(f"Anomalies: {results['summary']['anomalies']}")
```

##### `generate_report() -> str`

Generate a comprehensive audit report.

**Returns:**
- Path to the generated report file (Markdown format)

**Example:**
```python
report_path = agent.generate_report()
print(f"Report saved to: {report_path}")
```

---

### AuditLogger

Immutable audit logger for tracking all system events.

#### Constructor

```python
AuditLogger()
```

#### Methods

##### `log_artifact_creation(filename: str, file_hash: str, creator: str, version: int = 1, status: str = "active") -> None`

Log the creation of a new artifact.

**Example:**
```python
logger = AuditLogger()
logger.log_artifact_creation(
    filename="logo.png",
    file_hash="abc123...",
    creator="Designer123",
    version=1,
    status="active"
)
```

##### `log_artifact_modification(filename: str, file_hash: str, modifier: str, description: str, previous_hash: str, version: int) -> None`

Log a modification to an existing artifact.

##### `log_incident(incident_type: str, filename: str, suspicious_actor: str, description: str, severity: str = "HIGH") -> None`

Log a security incident.

**Parameters:**
- `incident_type` (str): Type of incident
- `filename` (str): File involved
- `suspicious_actor` (str): Actor involved
- `description` (str): Incident description
- `severity` (str): Severity level (LOW, MEDIUM, HIGH, CRITICAL)

##### `get_audit_history() -> List[Dict[str, Any]]`

Get the complete audit history.

**Returns:**
- List of all audit log entries

##### `get_incident_history() -> List[Dict[str, Any]]`

Get the complete incident history.

**Returns:**
- List of all incident log entries

---

### AlertSystem

Alert system for notifying supervisors of important events.

#### Constructor

```python
AlertSystem()
```

#### Methods

##### `send_alert(level: AlertLevel, message: str, filename: str = None, actor: str = None) -> None`

Send an alert to the supervisor.

**Parameters:**
- `level` (AlertLevel): Severity level (LOW, MEDIUM, HIGH, CRITICAL)
- `message` (str): Alert message
- `filename` (str, optional): Related filename
- `actor` (str, optional): Related actor

**Example:**
```python
from pixarr_design.core.alerts import AlertSystem, AlertLevel

alerts = AlertSystem()
alerts.send_alert(
    level=AlertLevel.HIGH,
    message="Unauthorized modification detected",
    filename="logo.png",
    actor="UnknownUser"
)
```

##### `get_alert_history() -> List[Dict[str, Any]]`

Get the complete alert history.

##### `get_alerts_by_level(level: AlertLevel) -> List[Dict[str, Any]]`

Get alerts filtered by severity level.

---

### IntegrityValidator

Validator for file integrity and metadata verification.

#### Constructor

```python
IntegrityValidator()
```

#### Methods

##### `verify_file(file_path: str) -> Dict[str, Any]`

Verify the integrity of a single file.

**Parameters:**
- `file_path` (str): Path to the file

**Returns:**
- Dictionary with verification results:
  - `filename`: Name of the file
  - `status`: OK, MODIFIED, ERROR, or NO_METADATA
  - `valid`: Boolean indicating if file passed validation
  - `current_hash`: Current file hash
  - `stored_hash`: Hash from metadata (if available)

**Example:**
```python
validator = IntegrityValidator()
result = validator.verify_file("designs/active/logo.png")
if result["valid"]:
    print("File integrity verified")
else:
    print(f"Integrity issue: {result['message']}")
```

##### `verify_directory(directory_path: str) -> List[Dict[str, Any]]`

Verify all monitored files in a directory.

**Parameters:**
- `directory_path` (str): Path to the directory

**Returns:**
- List of verification results for all files

##### `get_anomalies() -> List[Dict[str, Any]]`

Get all files with integrity issues.

##### `get_summary() -> Dict[str, Any]`

Get a summary of validation results.

**Returns:**
- Dictionary with keys:
  - `total_files`: Total files validated
  - `valid_files`: Number of valid files
  - `anomalies`: Number of files with issues
  - `no_metadata`: Number of untracked files

---

## Utility Modules

### hash_utils

#### `calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str`

Calculate the hash of a file.

**Parameters:**
- `file_path` (str): Path to the file
- `algorithm` (str): Hash algorithm (default: "sha256")

**Returns:**
- Hexadecimal hash string

**Example:**
```python
from pixarr_design.utils.hash_utils import calculate_file_hash

file_hash = calculate_file_hash("logo.png")
print(f"SHA-256: {file_hash}")
```

#### `verify_file_integrity(file_path: str, expected_hash: str, algorithm: str = "sha256") -> bool`

Verify the integrity of a file by comparing its hash.

**Parameters:**
- `file_path` (str): Path to the file
- `expected_hash` (str): Expected hash value
- `algorithm` (str): Hash algorithm (default: "sha256")

**Returns:**
- True if hashes match, False otherwise

#### `calculate_string_hash(content: str, algorithm: str = "sha256") -> str`

Calculate the hash of a string.

---

### metadata

#### `inject_metadata(file_path: str, metadata: Dict[str, Any]) -> None`

Inject metadata into a file.

For PNG files, metadata is embedded directly into the image.
For other files, a separate .meta JSON file is created.

**Parameters:**
- `file_path` (str): Path to the target file
- `metadata` (dict): Metadata dictionary

**Example:**
```python
from pixarr_design.utils.metadata import inject_metadata

metadata = {
    "filename": "logo.png",
    "hash": "abc123...",
    "creator": "Designer123",
    "version": 1
}
inject_metadata("designs/active/logo.png", metadata)
```

#### `validate_metadata(file_path: str) -> Optional[Dict[str, Any]]`

Validate and extract metadata from a file.

**Parameters:**
- `file_path` (str): Path to the file

**Returns:**
- Metadata dictionary if found, None otherwise

**Example:**
```python
from pixarr_design.utils.metadata import validate_metadata

metadata = validate_metadata("designs/active/logo.png")
if metadata:
    print(f"Creator: {metadata['creator']}")
    print(f"Version: {metadata['version']}")
```

---

## Dashboard Module

### ReportGenerator

Generator for markdown audit reports.

#### Constructor

```python
ReportGenerator(
    audit_logger: AuditLogger,
    alert_system: AlertSystem,
    integrity_validator: IntegrityValidator
)
```

#### Methods

##### `generate_report(output_path: Optional[str] = None) -> str`

Generate a comprehensive markdown report.

**Parameters:**
- `output_path` (str, optional): Custom output path

**Returns:**
- Path to the generated report

**Example:**
```python
from pixarr_design.dashboard.generator import ReportGenerator

generator = ReportGenerator(logger, alerts, validator)
report_path = generator.generate_report()
```

---

## Configuration

### Settings

Global configuration for PixARR Design system.

#### Class Attributes

- `SUPERVISOR_NAME`: "Melampe001"
- `SUPERVISOR_EMAIL`: "tokraagcorp@gmail.com"
- `MONITORED_EXTENSIONS`: List of monitored file extensions
- `HASH_ALGORITHM`: "sha256"
- `HASH_BLOCK_SIZE`: 8192 bytes

#### Class Methods

##### `ensure_directories() -> None`

Create all required directories if they don't exist.

##### `is_monitored_file(filename: str) -> bool`

Check if a file should be monitored based on its extension.

**Example:**
```python
from pixarr_design.config.settings import Settings

if Settings.is_monitored_file("logo.png"):
    print("File is monitored")
```

---

## Data Formats

### Audit Log Entry

```json
{
  "type": "artifact_created",
  "timestamp": "2025-12-21T10:30:00Z",
  "filename": "logo.png",
  "hash": "6e3cf5a8b9d2f1c4...",
  "creator": "Designer123",
  "version": 1,
  "status": "active",
  "supervisor": "Melampe001"
}
```

### Incident Log Entry

```json
{
  "type": "unauthorized_access",
  "timestamp": "2025-12-21T10:35:00Z",
  "filename": "logo.png",
  "suspicious_actor": "UnknownUser",
  "description": "Acceso no autorizado detectado",
  "severity": "HIGH",
  "supervisor": "Melampe001"
}
```

### Metadata Format

```json
{
  "filename": "logo.png",
  "hash": "abc123...",
  "creator": "Designer123",
  "created_at": "2025-12-21T10:00:00Z",
  "version": 2,
  "status": "active",
  "supervisor": "Melampe001",
  "last_modified_by": "Designer456",
  "last_modified_at": "2025-12-21T10:30:00Z",
  "modification_description": "Updated colors",
  "previous_hash": "def456..."
}
```

---

*API Documentation - PixARR Design System v1.0*
