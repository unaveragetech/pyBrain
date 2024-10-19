# PyBrain: AI Communication and Learning System

## Overview

The **PyBrain** project contains several scripts designed to simulate communication between artificial intelligence (AI) brains and perform passive and active learning tasks. The system is built to continuously learn from inputs, passively monitor schemas, and actively engage in conversation or data collection tasks. This project also incorporates communication between multiple instances using secure webhooks.

## Scripts Overview

### 1. **APLS.py** - Active and Passive Learning System
This script focuses on **active** and **passive** learning. It combines two key functions:
- **Active Learning**: The system takes inputs from the user, asks clarifying questions, and stores the learned data for future interactions. This is akin to an AI training module where the system learns by interacting with the user.
- **Passive Learning**: The script monitors the existing knowledge schemas (previously learned topics) and, if a schema's strength falls below a certain threshold, it seeks out and gathers related information from external sources without alerting the user.

**Key Features**:
- Active interaction to build knowledge.
- Passive background learning to strengthen weak knowledge schemas.
- Dynamic question generation based on ambiguous user inputs.

### Run Procedure:
```bash
python APLS.py
```

### 2. **KTPM.py** - Knowledge Update through Passive Monitoring
This script expands on the **passive learning** idea by assessing the system's knowledge base, or schemas, and constantly checking whether the knowledge is strong enough. If a schema falls below a certain threshold, it triggers a search for related information from predefined web sources using **requests** and **BeautifulSoup**. The data collected is then integrated back into the system to reinforce learning.

**Key Features**:
- Schema assessment for knowledge strength.
- Automated background search and integration of new information.
- Continuous passive knowledge enhancement without user intervention.

### Run Procedure:
```bash
python KTPM.py
```

### 3. **FACE.py** - Face-to-Face Knowledge Comparison
This script creates a simulation where two instances of PyBrain can interact and share knowledge. **FACE.py** serves as a way for two systems to "talk" to each other, comparing their knowledge bases and determining the gaps or overlaps in what they know. This interaction can be useful for system learning and schema updates based on another instance's knowledge.

**Key Features**:
- System-to-system interaction.
- Knowledge comparison and schema update between two AI instances.
- Face-to-face simulation of AI conversation.

### Run Procedure:
```bash
python FACE.py
```

### 4. **brain_communication.py** - AI Brain Communication via Webhooks
The `brain_communication.py` script is designed to facilitate communication between two instances of PyBrain using secure webhooks. The script runs a local Flask server and allows the user to send messages between two brain instances, while verifying the authenticity of the communication using password-protected tokens.

**Streamlit** is used to provide a UI where the user can send messages and see the conversation between two instances. It also supports running on specific ports and using custom passwords for secure communication.

**Key Features**:
- Communication between two PyBrain instances using webhooks.
- Flask-based message handling with password verification.
- Streamlit UI for user interaction and live conversation display.
- Configurable ports and passwords for secure communication.

### Run Procedure (Default):
```bash
python brain_communication.py
```

### Run Procedure (Custom Port and Password):
```bash
python brain_communication.py --port 6000 --peer_port 6001 --password my_secret_password
```

## How the System Works
1. **Learning and Schema Updates**:
   - The **APLS.py** and **KTPM.py** scripts handle the learning aspect of the system, with active learning from user interactions and passive monitoring of schema strength for ongoing knowledge updates.
  
2. **Face-to-Face Knowledge Exchange**:
   - The **FACE.py** script allows two PyBrain instances to compare their knowledge, learning from each other’s databases.

3. **Communication Between Instances**:
   - The **brain_communication.py** script allows real-time communication between two PyBrain instances using webhooks secured by passwords. Users can interact with the system via the Streamlit UI.

## System Communication Security
The **brain_communication.py** script ensures secure communication by using password-protected tokens. Only the instances with the correct token can interact and share messages. This feature prevents unauthorized access to the communication pipeline.

## Conclusion
The **PyBrain** project is designed to simulate human-like learning and communication between AI systems. Each script in this repository plays a role in either active learning, passive schema monitoring, or real-time knowledge exchange between instances. Whether running the system to passively monitor learning or facilitating a secure conversation between two instances, this framework is designed for continuous and evolving AI learning.

