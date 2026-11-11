import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

SCREENSHOTS_DIR = r"c:\Users\AMAN KUMAR SINGH\Pictures\Screenshots"

# Set high DPI and aesthetic styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# 1. DFD LEVEL 0 (Context Level Diagram)
# ==============================================================================
def create_dfd_level_0():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "DATA FLOW DIAGRAM (DFD) - LEVEL 0: CONTEXT DIAGRAM", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')
    ax.text(50, 90, "System Boundary, External Entities and Primary Ingestion Flows", 
            ha='center', va='center', fontsize=9, color='#64748B')

    # External Entity: Candidate / Recruiter (Left)
    ent1 = patches.FancyBboxPatch((4, 45), 20, 22, boxstyle="round,pad=1.5", 
                                  fc='#FFFFFF', ec='#3B82F6', lw=2)
    ax.add_patch(ent1)
    ax.text(14, 58, "EXTERNAL ENTITY", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#2563EB')
    ax.text(14, 53, "Candidate /\nRecruiter", ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A')

    # Central Process: 0.0 AI Resume Analyzer Platform (Center Circle)
    proc = patches.Circle((50, 56), 16, fc='#FFFFFF', ec='#4F46E5', lw=2.5)
    ax.add_patch(proc)
    ax.text(50, 63, "PROCESS 0.0", ha='center', va='center', fontsize=8, fontweight='bold', color='#4F46E5')
    ax.text(50, 56, "AI Powered\nResume Analyzer\nDevOps System", ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A')

    # External Entity: DevOps Engineer / Admin (Top)
    ent2 = patches.FancyBboxPatch((40, 10), 20, 16, boxstyle="round,pad=1.5", 
                                  fc='#FFFFFF', ec='#10B981', lw=2)
    ax.add_patch(ent2)
    ax.text(50, 20, "ADMIN ENTITY", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#059669')
    ax.text(50, 15, "DevOps Engineer\n(Git Commits)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')

    # External Entity: Observability Tier (Right)
    ent3 = patches.FancyBboxPatch((76, 45), 20, 22, boxstyle="round,pad=1.5", 
                                  fc='#FFFFFF', ec='#F59E0B', lw=2)
    ax.add_patch(ent3)
    ax.text(86, 58, "MONITORING TIER", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#D97706')
    ax.text(86, 53, "Nagios Core\nHealth Daemon", ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A')

    # Data Flow Arrows & Labels
    # User -> System
    ax.annotate("", xy=(34, 58), xytext=(24, 58),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2, mutation_scale=15))
    ax.text(29, 62, "1. PDF Resume &\nJob Description", ha='center', va='bottom', fontsize=8, color="#1E3A8A", fontweight='bold')

    # System -> User
    ax.annotate("", xy=(24, 52), xytext=(34, 52),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=15))
    ax.text(29, 45, "2. Score (0-100%), Skills &\nRecruiter Feedback", ha='center', va='top', fontsize=8, color="#065F46", fontweight='bold')

    # Admin -> System
    ax.annotate("", xy=(50, 40), xytext=(50, 26),
                arrowprops=dict(arrowstyle="->", color="#10B981", lw=2, mutation_scale=15))
    ax.text(51, 33, " 3. Code & Manifest Updates", ha='left', va='center', fontsize=8, color="#047857", fontweight='bold')

    # System <-> Nagios
    ax.annotate("", xy=(76, 58), xytext=(66, 58),
                arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=2, mutation_scale=15))
    ax.text(71, 62, "4. Synthetic Probes\n(ICMP/HTTP)", ha='center', va='bottom', fontsize=8, color="#B45309", fontweight='bold')

    ax.annotate("", xy=(66, 52), xytext=(76, 52),
                arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=2, mutation_scale=15))
    ax.text(71, 45, "5. Telemetry Status\n(HTTP 200 OK)", ha='center', va='top', fontsize=8, color="#B45309", fontweight='bold')

    out_path = os.path.join(SCREENSHOTS_DIR, "diagram_dfd_level_0.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved DFD Level 0 to:", out_path)

# ==============================================================================
# 2. DFD LEVEL 1 (Decomposed Process Flow Diagram)
# ==============================================================================
def create_dfd_level_1():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "DATA FLOW DIAGRAM (DFD) - LEVEL 1: DETAILED PROCESS DECOMPOSITION", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')

    # Process 1.0: Document Intake & PDF Parsing
    p1 = patches.FancyBboxPatch((5, 68), 24, 18, boxstyle="round,pad=1", fc='#FFFFFF', ec='#3B82F6', lw=1.8)
    ax.add_patch(p1)
    ax.text(17, 80, "PROCESS 1.0", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#2563EB')
    ax.text(17, 74, "Multipart PDF Ingestion\n& Text Extraction", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Process 2.0: AI Semantic Scoring Engine (Gemini LLM)
    p2 = patches.FancyBboxPatch((38, 68), 24, 18, boxstyle="round,pad=1", fc='#FFFFFF', ec='#8B5CF6', lw=1.8)
    ax.add_patch(p2)
    ax.text(50, 80, "PROCESS 2.0", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#7C3AED')
    ax.text(50, 74, "Gemini 1.5 Flash LLM\nSemantic Analysis", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Process 3.0: Data Persistence & Auditing
    p3 = patches.FancyBboxPatch((71, 68), 24, 18, boxstyle="round,pad=1", fc='#FFFFFF', ec='#10B981', lw=1.8)
    ax.add_patch(p3)
    ax.text(83, 80, "PROCESS 3.0", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#059669')
    ax.text(83, 74, "Evaluation Store\n(MongoDB Atlas)", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Process 4.0: CI/CD Pipeline Automation (Jenkins)
    p4 = patches.FancyBboxPatch((5, 20), 24, 18, boxstyle="round,pad=1", fc='#FFFFFF', ec='#EF4444', lw=1.8)
    ax.add_patch(p4)
    ax.text(17, 32, "PROCESS 4.0", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#DC2626')
    ax.text(17, 26, "Jenkins Automated\nCI/CD Pipeline", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Process 5.0: Docker Container Deployment (AWS EC2)
    p5 = patches.FancyBboxPatch((38, 20), 24, 18, boxstyle="round,pad=1", fc='#FFFFFF', ec='#0EA5E9', lw=1.8)
    ax.add_patch(p5)
    ax.text(50, 32, "PROCESS 5.0", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0284C7')
    ax.text(50, 26, "Docker Microservices\n(AWS EC2 Host)", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Process 6.0: Nagios Active Health Telemetry
    p6 = patches.FancyBboxPatch((71, 20), 24, 18, boxstyle="round,pad=1", fc='#FFFFFF', ec='#F59E0B', lw=1.8)
    ax.add_patch(p6)
    ax.text(83, 32, "PROCESS 6.0", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#D97706')
    ax.text(83, 26, "Nagios Synthetic\nHealth Telemetry", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Flow arrows
    # P1 -> P2
    ax.annotate("", xy=(38, 77), xytext=(29, 77),
                arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.8, mutation_scale=14))
    ax.text(33.5, 80, "Raw Text\nBuffer", ha='center', va='bottom', fontsize=7.5, color="#1D4ED8", fontweight='bold')

    # P2 -> P3
    ax.annotate("", xy=(71, 77), xytext=(62, 77),
                arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.8, mutation_scale=14))
    ax.text(66.5, 80, "JSON Score &\nSkills", ha='center', va='bottom', fontsize=7.5, color="#6D28D9", fontweight='bold')

    # P4 -> P5
    ax.annotate("", xy=(38, 29), xytext=(29, 29),
                arrowprops=dict(arrowstyle="->", color="#EF4444", lw=1.8, mutation_scale=14))
    ax.text(33.5, 32, "Docker\nCompose Up", ha='center', va='bottom', fontsize=7.5, color="#B91C1C", fontweight='bold')

    # P5 <-> P6
    ax.annotate("", xy=(71, 29), xytext=(62, 29),
                arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=1.8, mutation_scale=14))
    ax.text(66.5, 32, "Polls\n/health", ha='center', va='bottom', fontsize=7.5, color="#B45309", fontweight='bold')

    # Vertical Link: P5 deploys runtime that executes P1 & P2
    ax.annotate("", xy=(17, 68), xytext=(17, 38),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5, ls="--", mutation_scale=12))
    ax.text(18, 53, "Runs Node.js &\nReact Containers", ha='left', va='center', fontsize=7.5, color="#0369A1")

    out_path = os.path.join(SCREENSHOTS_DIR, "diagram_dfd_level_1.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved DFD Level 1 to:", out_path)

# ==============================================================================
# 3. ENTERPRISE DEVOPS PIPELINE ARCHITECTURE DIAGRAM
# ==============================================================================
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 95, "DEVOPS LIFECYCLE & INFRASTRUCTURE PIPELINE ARCHITECTURE", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')

    # Box 1: SCM
    b1 = patches.FancyBboxPatch((3, 40), 16, 32, boxstyle="round,pad=1", fc='#FFFFFF', ec='#334155', lw=1.8)
    ax.add_patch(b1)
    ax.text(11, 66, "SOURCE CONTROL", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#64748B')
    ax.text(11, 56, "GitHub\nRepository", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(11, 46, "Code • Tests\nManifests", ha='center', va='center', fontsize=8, color='#475569')

    # Box 2: CI/CD Jenkins
    b2 = patches.FancyBboxPatch((24, 40), 18, 32, boxstyle="round,pad=1", fc='#FFFFFF', ec='#DC2626', lw=1.8)
    ax.add_patch(b2)
    ax.text(33, 66, "CI/CD ORCHESTRATOR", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#DC2626')
    ax.text(33, 56, "Jenkins Engine\n(Jenkinsfile)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(33, 46, "1. Test (Jest)\n2. Build Images\n3. Deploy", ha='center', va='center', fontsize=8, color='#475569')

    # Box 3: Cloud Infrastructure (AWS EC2)
    b3 = patches.FancyBboxPatch((47, 25), 32, 55, boxstyle="round,pad=1.5", fc='#FFFFFF', ec='#2563EB', lw=2)
    ax.add_patch(b3)
    ax.text(63, 74, "AWS EC2 CLOUD COMPUTE (UBUNTU 24.04)", ha='center', va='center', fontsize=8, fontweight='bold', color='#1D4ED8')

    # Inside EC2: Microservices
    c1 = patches.FancyBboxPatch((49, 58), 28, 12, boxstyle="round,pad=0.5", fc='#EFF6FF', ec='#3B82F6', lw=1.2)
    ax.add_patch(c1)
    ax.text(63, 64, "Docker: ReactJS Web Dashboard (Port 80)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E40AF')

    c2 = patches.FancyBboxPatch((49, 44), 28, 12, boxstyle="round,pad=0.5", fc='#F5F3FF', ec='#8B5CF6', lw=1.2)
    ax.add_patch(c2)
    ax.text(63, 50, "Docker: Node.js Express REST API (Port 5000)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#5B21B6')

    c3 = patches.FancyBboxPatch((49, 30), 28, 12, boxstyle="round,pad=0.5", fc='#ECFDF5', ec='#10B981', lw=1.2)
    ax.add_patch(c3)
    ax.text(63, 36, "Database: MongoDB Atlas Cloud Cluster", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46')

    # Box 4: Monitoring (Nagios)
    b4 = patches.FancyBboxPatch((83, 40), 14, 32, boxstyle="round,pad=1", fc='#FFFFFF', ec='#F59E0B', lw=1.8)
    ax.add_patch(b4)
    ax.text(90, 66, "MONITORING", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#D97706')
    ax.text(90, 56, "Nagios Core\nDashboard", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(90, 46, "Port 8085\nAll OK (Green)", ha='center', va='center', fontsize=8, color='#059669', fontweight='bold')

    # Connecting Arrows
    ax.annotate("", xy=(24, 56), xytext=(19, 56),
                arrowprops=dict(arrowstyle="->", color="#334155", lw=2, mutation_scale=14))
    ax.annotate("", xy=(47, 56), xytext=(42, 56),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2, mutation_scale=14))
    ax.annotate("", xy=(83, 56), xytext=(79, 56),
                arrowprops=dict(arrowstyle="<->", color="#F59E0B", lw=2, mutation_scale=14))

    # Terraform & Puppet side indicators
    ax.text(63, 16, "Provisioned by Terraform (IaC)  |  Hardened by Puppet (site.pp)", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#475569')

    out_path = os.path.join(SCREENSHOTS_DIR, "diagram_architecture_pipeline.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved Architecture Pipeline Diagram to:", out_path)

create_dfd_level_0()
create_dfd_level_1()
create_architecture_diagram()
print("All diagram graphics successfully generated!")
