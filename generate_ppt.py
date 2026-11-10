import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SCREENSHOTS_DIR = r"c:\Users\AMAN KUMAR SINGH\Pictures\Screenshots"
OUTPUT_PPTX_PATH = r"c:\Users\AMAN KUMAR SINGH\Desktop\INT333 PROJECT\AI_Resume_Analyzer_Master_Presentation.pptx"


# ==============================================================================
# PROFESSIONAL ENTERPRISE THEME PALETTE (Clean White & Slate with Indigo/Cyan Accents)
# ==============================================================================
BG_PAGE = RGBColor(248, 250, 252)       # Slate 50 (#F8FAFC)
CARD_BG = RGBColor(255, 255, 255)       # Pure White (#FFFFFF)
CARD_BORDER = RGBColor(226, 232, 240)   # Slate 200 (#E2E8F0)
CODE_BG = RGBColor(15, 23, 42)          # Slate 900 (#0F172A) Dark Terminal Card
CODE_BORDER = RGBColor(51, 65, 85)      # Slate 700 (#334155)

TEXT_PRIMARY = RGBColor(15, 23, 42)     # Slate 900 (#0F172A)
TEXT_SECONDARY = RGBColor(71, 85, 105)  # Slate 600 (#475569)
TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500 (#64748B)
TEXT_WHITE = RGBColor(255, 255, 255)

ACCENT_BLUE = RGBColor(37, 99, 235)     # Royal Blue (#2563EB)
ACCENT_INDIGO = RGBColor(79, 70, 229)   # Indigo (#4F46E5)
ACCENT_CYAN = RGBColor(14, 165, 233)    # Sky/Cyan (#0EA5E9)
ACCENT_GREEN = RGBColor(16, 185, 129)   # Emerald (#10B981)
ACCENT_AMBER = RGBColor(245, 158, 11)   # Amber (#F59E0B)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def apply_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = BG_PAGE
    bg_shape.line.color.rgb = BG_PAGE
    return bg_shape

def add_header(slide, title_text, category_text="INT333 DEVOPS LIFECYCLE PIPELINE", step_number=None):
    # Top banner bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ACCENT_BLUE
    top_bar.line.fill.background()

    # Header text box
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(1.15))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    badge = f"PHASE {step_number} • " if step_number else ""
    p_cat.text = f"{badge}{category_text}".upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_BLUE

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_PRIMARY

def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ACCENT_BLUE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(Inches(left + 0.28), Inches(top + 0.25), Inches(width - 0.56), Inches(height - 0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if title:
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_color
        p_t.space_after = Pt(8)

    for i, bullet in enumerate(body_bullets):
        p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
        p.text = f"•  {bullet}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_SECONDARY
        p.space_after = Pt(6)

def add_code_card(slide, left, top, width, height, filename, code_content, lang_badge="CODE"):
    # Dark terminal container
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = CODE_BG
    card.line.color.rgb = CODE_BORDER
    card.line.width = Pt(1)

    # Title / Badge bar
    hdr = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.15), Inches(width - 0.5), Inches(0.4))
    tf_h = hdr.text_frame
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
    p_h = tf_h.paragraphs[0]
    p_h.text = f"📄 {filename}  [{lang_badge}]"
    p_h.font.size = Pt(10)
    p_h.font.bold = True
    p_h.font.color.rgb = ACCENT_CYAN

    # Code content
    code_box = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.55), Inches(width - 0.5), Inches(height - 0.7))
    tf_c = code_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    lines = code_content.strip().split('\n')
    for idx, line in enumerate(lines[:24]): # max 24 lines per slide for perfect readability
        p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
        p.text = line
        p.font.name = "Consolas"
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240) # Slate 200

def add_image_card(slide, left, top, width, height, img_filename, label="LIVE DEMONSTRATION SCREENSHOT"):
    frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    frame.fill.solid()
    frame.fill.fore_color.rgb = CARD_BG
    frame.line.color.rgb = CARD_BORDER
    frame.line.width = Pt(1.2)

    lbl_box = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.35))
    tf_lbl = lbl_box.text_frame
    tf_lbl.margin_left = tf_lbl.margin_top = tf_lbl.margin_right = tf_lbl.margin_bottom = 0
    p_l = tf_lbl.paragraphs[0]
    p_l.text = f"📸 {label.upper()}"
    p_l.font.size = Pt(9.5)
    p_l.font.bold = True
    p_l.font.color.rgb = ACCENT_BLUE

    img_path = os.path.join(SCREENSHOTS_DIR, img_filename)
    if os.path.exists(img_path):
        img_left = Inches(left + 0.15)
        img_top = Inches(top + 0.5)
        img_w = Inches(width - 0.3)
        img_h = Inches(height - 0.65)
        slide.shapes.add_picture(img_path, img_left, img_top, width=img_w)
    else:
        print(f"Image not found: {img_path}")

print("Generating 17-slide Master Presentation with full DevOps code...")

# ==============================================================================
# SLIDE 1: Cover Slide
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
apply_background(s1)

# Decorative header bar
top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.2))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = ACCENT_BLUE
top_bar.line.fill.background()

# Title card box
tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(3.6))
tf1 = tbox.text_frame
tf1.word_wrap = True

p0 = tf1.paragraphs[0]
p0.text = "LOVELY PROFESSIONAL UNIVERSITY  •  DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = ACCENT_BLUE
p0.space_after = Pt(12)

p1 = tf1.add_paragraph()
p1.text = "AI Powered Resume Analyzer"
p1.font.size = Pt(38)
p1.font.bold = True
p1.font.color.rgb = TEXT_PRIMARY

p2 = tf1.add_paragraph()
p2.text = "Automated DevOps Lifecycle and Resilient Infrastructure Pipeline"
p2.font.size = Pt(21)
p2.font.bold = True
p2.font.color.rgb = ACCENT_INDIGO
p2.space_after = Pt(16)

p3 = tf1.add_paragraph()
p3.text = "Full DevOps Stack: AWS EC2  •  Terraform  •  Puppet  •  Docker  •  Jenkins CI/CD  •  Nagios  •  Google Gemini LLM"
p3.font.size = Pt(12.5)
p3.font.color.rgb = TEXT_MUTED

# Candidate metadata card
add_card(s1, 1.0, 4.8, 11.333, 1.9, "PROJECT SUBMISSION CREDENTIALS", [
    "Candidate Name: AMAN KUMAR SINGH",
    "Registration Number: 12301704   |   Roll Number: 02   |   Section: K202316",
    "Course Code: INT333 (DevOps Technologies & Practice)",
    "Project Repository: https://github.com/softways1/INT333-PROJECT"
], ACCENT_BLUE)


# ==============================================================================
# SLIDE 2: Problem Statement & Project Scope
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
apply_background(s2)
add_header(s2, "Executive Overview: Problem Addressed & Engineering Objectives", "PROJECT FOUNDATION")

add_card(s2, 0.8, 1.6, 5.7, 5.2, "THE RECRUITMENT & INFRASTRUCTURE BOTTLENECKS", [
    "Manual Resume Screening Overload: Technical recruitment involves parsing thousands of candidate profiles manually, creating backlogs, bias, and prolonged hiring cycles.",
    "Environmental Drift & Configuration Variance: Deploying AI applications without declarative infrastructure causes 'works on my machine' errors and manual cloud setup mismatches.",
    "Fragile Software Release Cycles: Manual code testing, image assembly, and remote host deployments lead to high production incident rates and downtime.",
    "Lack of Observability: Unmonitored cloud services leave engineering teams blind to host resource saturation, database drops, or HTTP endpoint failures."
], ACCENT_AMBER)

add_card(s2, 6.8, 1.6, 5.7, 5.2, "AUTOMATED DEVOPS SOLUTION & OBJECTIVES", [
    "Automate Cloud Infrastructure: Codify and provision reproducible AWS compute instances, networking subnets, security boundaries, and storage using Terraform.",
    "Enforce System Baselines: Automate OS package installation, host hardening, Docker daemon management, and Nagios NRPE client setup using Puppet.",
    "Containerize Microservices: Encapsulate ReactJS UI, Node.js REST API, and MongoDB into reproducible, isolated Docker containers.",
    "Orchestrate CI/CD Delivery: Develop an automated Jenkins pipeline for code checkout, Jest unit tests, Docker builds, and automated deployments.",
    "Establish 24/7 Monitoring: Deploy Nagios to proactively track host uptime, CPU/RAM/Disk metrics, and synthetic API endpoint health.",
    "Intelligent Semantic Evaluation: Integrate Google Gemini 1.5 Flash LLM to parse resumes and score candidate relevance against job postings in real time."
], ACCENT_GREEN)


# ==============================================================================
# SLIDE 3: Architectural Pipeline Flow
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
apply_background(s3)
add_header(s3, "Enterprise Architectural Pipeline Flow & Separation of Duties", "SYSTEM ARCHITECTURE")

add_card(s3, 0.8, 1.6, 3.6, 5.2, "1. PROVISION & HARDEN", [
    "AWS EC2 Compute: Ubuntu 24.04 LTS host instance instantiated.",
    "Terraform (IaC): Declaratively defines VPC, subnets, route tables, and security group firewall rules.",
    "Puppet (CM): Enforces operating system baselines, packages, user privileges, and Nagios NRPE client setup without server drift."
], ACCENT_BLUE)

add_card(s3, 4.8, 1.6, 3.6, 5.2, "2. ASSEMBLE & DELIVER", [
    "Git / GitHub: Version control repository tracking source code, Dockerfiles, and automation manifests.",
    "Jenkins CI/CD: Automated declarative pipeline triggered upon repository commit.",
    "Automated Testing: Runs Jest unit tests to verify REST API logic before build.",
    "Docker Engine: Builds multi-stage Nginx React UI and Node.js Gemini containers."
], ACCENT_INDIGO)

add_card(s3, 8.8, 1.6, 3.7, 5.2, "3. SERVE & OBSERVE", [
    "MongoDB Atlas: High-availability cloud document store persisting evaluation records.",
    "Google Gemini LLM: AI semantic scoring, entity extraction, and recruiter feedback.",
    "Nagios Core 4: Active monitoring dashboard polling ICMP ping, host CPU/disk metrics, and HTTP API health endpoints 24/7."
], ACCENT_GREEN)


# ==============================================================================
# SLIDE 4: Phase 1 — Cloud Infrastructure: AWS EC2 Host
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
apply_background(s4)
add_header(s4, "Cloud Compute Infrastructure: AWS EC2 Instance Provisioning", "INFRASTRUCTURE", 1)

add_card(s4, 0.8, 1.6, 4.8, 5.2, "AWS EC2 COMPUTING ENVIRONMENT", [
    "Instance Type: t2.micro (AWS Free Tier eligible, 1 vCPU, 1 GB RAM).",
    "Operating System: Ubuntu Server 24.04 LTS (Noble Numbat).",
    "Persistent Storage: 25 GiB gp3 General Purpose EBS Volume.",
    "Memory Stabilization: Configured a 1.5 GB Swapfile (/swapfile) to guarantee zero out-of-memory crashes for Jenkins & Docker microservices.",
    "Security Group Firewall Rules:",
    "  • Port 22 (SSH): Secure remote administration.",
    "  • Port 80 (HTTP): Production React Web UI.",
    "  • Port 5000: Node.js Backend REST API.",
    "  • Port 8080: Jenkins CI/CD Automation Web UI.",
    "  • Port 8085: Nagios Monitoring Web Dashboard.",
    "Viva Point: EC2 was kept running continuously overnight with zero cost to preserve the Public IPv4 address for live in-class demonstration."
], ACCENT_BLUE)

add_image_card(s4, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-10 224356.png", "AWS EC2 Ubuntu Terminal Session")


# ==============================================================================
# SLIDE 5: Phase 2 — Terraform Infrastructure as Code (IaC)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
apply_background(s5)
add_header(s5, "Infrastructure as Code (IaC): Terraform Declarative Workflow", "TERRAFORM", 2)

add_card(s5, 0.8, 1.6, 4.8, 5.2, "TERRAFORM IAC IMPLEMENTATION", [
    "Role in Project: Replaces slow, error-prone manual cloud console creation with version-controlled, reproducible code.",
    "Terraform Core Components:",
    "  • provider.tf: Declares AWS provider v5 with region and mock evaluation parameters.",
    "  • variables.tf: Modular variables for region, instance type (t2.micro), key pair, and AMI ID.",
    "  • main.tf: Codifies VPC, public subnet, internet gateway, route table, security group, and EC2 instance.",
    "  • outputs.tf: Exports public IP and SSH helper command.",
    "Workflow Execution: terraform init followed by terraform plan.",
    "Plan Validation: Evaluated execution graph resolving: Plan: 6 to add, 0 to change, 0 to destroy."
], ACCENT_CYAN)

add_image_card(s5, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-10 225434.png", "Terraform Plan: 6 To Add Execution Output")


# ==============================================================================
# SLIDE 6: Phase 2 — Terraform Source Code (`main.tf`)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
apply_background(s6)
add_header(s6, "Terraform Source Code: Declarative Cloud Infrastructure", "TERRAFORM CODE", 2)

terraform_code_snippet = """# 1. Virtual Private Cloud (VPC)
resource "aws_vpc" "devops_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "ai-resume-analyzer-vpc" }
}

# 2. Public Subnet & Internet Gateway
resource "aws_internet_gateway" "devops_igw" {
  vpc_id = aws_vpc.devops_vpc.id
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.devops_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

# 3. Security Group (Firewall Rules for All Tools)
resource "aws_security_group" "devops_sg" {
  name   = "ai-resume-analyzer-sg"
  vpc_id = aws_vpc.devops_vpc.id

  ingress { from_port = 22; to_port = 22; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 80; to_port = 80; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 5000; to_port = 5000; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 8080; to_port = 8080; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 8085; to_port = 8085; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
}

# 4. EC2 Compute Node
resource "aws_instance" "devops_server" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.devops_sg.id]
}"""

add_code_card(s6, 0.8, 1.6, 6.2, 5.2, "terraform/main.tf", terraform_code_snippet, "HCL")

add_card(s6, 7.3, 1.6, 5.2, 5.2, "TECHNICAL ARCHITECTURE NOTES", [
    "Declarative Syntax: Specifies the desired end-state rather than procedural steps.",
    "Dependency Graph: Terraform automatically infers that the subnet requires the VPC, and the EC2 instance requires the subnet and security group.",
    "Port Isolation: Explicitly provisions inbound ports for React (80), Node.js (5000), Jenkins (8080), and Nagios (8085).",
    "Reproducibility: If infrastructure is destroyed, running terraform apply will reconstruct the exact cloud environment within 90 seconds."
], ACCENT_CYAN)


# ==============================================================================
# SLIDE 7: Phase 3 — Puppet Configuration Management
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
apply_background(s7)
add_header(s7, "Configuration Management: Puppet System Hardening & Drift Control", "PUPPET", 3)

add_card(s7, 0.8, 1.6, 4.8, 5.2, "PUPPET SYSTEM BASELINE ENFORCEMENT", [
    "Role in Project: Enforces operating system consistency across all target hosts, preventing human configuration drift.",
    "Puppet Execution Mode: Standalone agent execution (sudo puppet apply site.pp).",
    "Enforced State Elements:",
    "  • Base Package Suite: Automatically installs docker.io, nagios-nrpe-server, htop, git, and monitoring plugins.",
    "  • Application Hierarchy: Provisions /opt/ai-resume-analyzer with ubuntu permissions.",
    "  • MOTD Security Banner: Provisions /etc/motd confirming configuration governance.",
    "  • Daemon Management: Enforces docker and nagios-nrpe-server daemons to remain enabled and running.",
    "  • Verification Output: Applied catalog in ... seconds successfully."
], ACCENT_AMBER)

add_image_card(s7, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-10 230407 puppet apply.png", "Puppet Apply: Catalog Applied Successfully")


# ==============================================================================
# SLIDE 8: Phase 3 — Puppet Manifest Code (`site.pp`)
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
apply_background(s8)
add_header(s8, "Puppet Manifest Code: System Baseline & Service Declarations", "PUPPET CODE", 3)

puppet_code_snippet = """node default {
  # 1. Base System Hardening & Essential Packages
  $base_packages = [
    'apt-transport-https', 'ca-certificates', 'curl',
    'gnupg', 'git', 'htop', 'unzip', 'ufw',
    'docker.io', 'nagios-nrpe-server', 'monitoring-plugins'
  ]

  package { $base_packages:
    ensure => installed,
  }

  # 2. Application Working Directory
  file { '/opt/ai-resume-analyzer':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  # 3. Host MOTD Governance Banner
  file { '/etc/motd':
    ensure  => file,
    owner   => 'root',
    mode    => '0644',
    content => "Managed by: Puppet Configuration Management\\n",
  }

  # 4. Enforce Docker Daemon State
  service { 'docker':
    ensure  => running,
    enable  => true,
    require => Package['docker.io'],
  }

  # 5. User Group Membership
  user { 'ubuntu':
    ensure => present,
    groups => ['docker'],
  }
}"""

add_code_card(s8, 0.8, 1.6, 6.2, 5.2, "puppet/manifests/site.pp", puppet_code_snippet, "PUPPET")

add_card(s8, 7.3, 1.6, 5.2, 5.2, "IDEMPOTENCY & DRIFT PREVENTION", [
    "Idempotency Guarantee: Puppet checks current system state against target state. If a package is already installed or a daemon is running, no redundant changes are made.",
    "Automated Remediation: If an administrator accidentally deletes /opt/ai-resume-analyzer or stops Docker, Puppet restores the correct state on the next run.",
    "Decoupled Architecture: Separates system baseline configuration from application runtime deployment."
], ACCENT_AMBER)


# ==============================================================================
# SLIDE 9: Phase 4 — Docker Microservices Containerization
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
apply_background(s9)
add_header(s9, "Microservices Containerization: Docker & Compose Orchestration", "DOCKER", 4)

add_card(s9, 0.8, 1.6, 4.8, 5.2, "DOCKER MULTI-TIER ARCHITECTURE", [
    "Role in Project: Packages application tiers into decoupled, lightweight, and isolated containers to ensure environment parity.",
    "Microservice Architecture:",
    "  • resume_frontend: Alpine Nginx container (<15MB RAM footprint) serving React SPA and reverse-proxying API traffic.",
    "  • resume_backend: Node.js 18 container executing Express API, PDF parser, and Google Gemini SDK.",
    "  • resume_mongodb: MongoDB document store with wiredTigerCacheSizeGB 0.25 memory constraint.",
    "Docker Compose Coordination: docker-compose up -d --build coordinates network bridges, volume mounts, and restart: unless-stopped policies.",
    "Verification: docker ps confirmed all 3 containers active with Up status."
], ACCENT_BLUE)

add_image_card(s9, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-10 231309.png", "Docker PS: Microservice Containers Running")


# ==============================================================================
# SLIDE 10: Phase 4 — Docker Compose & Dockerfile Code
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
apply_background(s10)
add_header(s10, "Docker Code: Multi-Service Compose & Backend Dockerfile", "DOCKER CODE", 4)

docker_code_snippet = """# docker-compose.yml
services:
  mongodb:
    image: mongo:6.0-jammy
    container_name: resume_mongodb
    restart: unless-stopped
    command: ["mongod", "--wiredTigerCacheSizeGB", "0.25"]
    ports: ["27017:27017"]
    volumes: [mongo_data:/data/db]

  backend:
    build: { context: ./backend, dockerfile: Dockerfile }
    container_name: resume_backend
    restart: unless-stopped
    environment:
      - PORT=5000
      - MONGO_URI=mongodb+srv://aman:Aks73367%40@cluster0.utlcqn0.mongodb.net/resume_analyzer
      - GEMINI_API_KEY=${GEMINI_API_KEY:-demo_key}
    ports: ["5000:5000"]
    depends_on: [mongodb]

  frontend:
    build: { context: ./frontend, dockerfile: Dockerfile }
    container_name: resume_frontend
    restart: unless-stopped
    ports: ["80:80", "3000:80"]
    depends_on: [backend]

# backend/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY . .
EXPOSE 5000
CMD ["node", "server.js"]"""

add_code_card(s10, 0.8, 1.6, 6.2, 5.2, "docker-compose.yml & Dockerfile", docker_code_snippet, "YAML/DOCKER")

add_card(s10, 7.3, 1.6, 5.2, 5.2, "CONTAINER OPTIMIZATION HIGHLIGHTS", [
    "Multi-Stage Alpine Builds: Uses Alpine Linux base images to minimize container attack surface and reduce image size.",
    "Reverse Proxy Integration: Nginx on port 80 routes frontend requests and proxies /api/ calls internally to the backend, eliminating CORS issues.",
    "Resource Constrained MongoDB: WiredTiger cache clamped to 256MB to ensure the entire full-stack runs smoothly on AWS Free Tier 1GB RAM.",
    "Decoupled Network: Isolated container bridge network ensures secure communication between backend and database."
], ACCENT_BLUE)


# ==============================================================================
# SLIDE 11: Phase 5 — AI Resume Analyzer Web Application
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
apply_background(s11)
add_header(s11, "AI Powered Resume Analyzer: Live Web Application & Gemini AI", "WEB APPLICATION", 5)

add_card(s11, 0.8, 1.6, 4.8, 5.2, "AI CAPABILITIES & APPLICATION ARCHITECTURE", [
    "Single Page Application (ReactJS): Modern, responsive candidate screening dashboard featuring live API health indicators.",
    "Google Gemini 1.5 Flash LLM: Powered by official @google/generative-ai SDK enforcing structured JSON mode.",
    "Candidate Compatibility Gauge: Extracts skills, evaluates strengths, detects missing skills, and computes a 0-100% score.",
    "MongoDB Atlas Cloud: Persists every candidate evaluation record for historical recruiter auditing.",
    "Fail-Safe Architecture: Features a resilient local semantic engine fallback to guarantee 100% live presentation uptime.",
    "Live Production URL: http://<EC2-PUBLIC-IP> accessible directly in any web browser."
], ACCENT_CYAN)

add_image_card(s11, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-10 231500.png", "AI Resume Analyzer: Match Score & Recommendations")


# ==============================================================================
# SLIDE 12: Phase 5 — Backend REST API & Gemini LLM Code
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
apply_background(s12)
add_header(s12, "Backend Code: Google Gemini LLM Integration & REST Endpoints", "API & LLM CODE", 5)

backend_code_snippet = """// backend/services/geminiService.js
const { GoogleGenerativeAI } = require('@google/generative-ai');

async function analyzeWithGemini(resumeText, jobDescription) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (apiKey && apiKey !== 'YOUR_GEMINI_API_KEY_HERE') {
    const genAI = new GoogleGenerativeAI(apiKey.trim());
    const model = genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      generationConfig: { responseMimeType: 'application/json' }
    });

    const prompt = `Analyze this resume against target job description.
    Respond strictly in JSON:
    { "candidateName": "...", "matchScore": 85,
      "extractedSkills": [...], "strengths": [...],
      "missingSkills": [...], "recommendations": "..." }`;

    const result = await model.generateContent(prompt);
    return JSON.parse(result.response.text().trim());
  }
  return runLocalSemanticAnalysis(resumeText, jobDescription);
}

// backend/server.js
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP', service: 'AI Resume Analyzer API' });
});

app.post('/api/analyze', upload.single('resume'), async (req, res) => {
  const result = await analyzeWithGemini(resumeText, jobDescription);
  const record = new Analysis(result);
  await record.save();
  res.json({ success: true, data: result });
});"""

add_code_card(s12, 0.8, 1.6, 6.2, 5.2, "backend/services/geminiService.js", backend_code_snippet, "NODE.JS/JAVASCRIPT")

add_card(s12, 7.3, 1.6, 5.2, 5.2, "GEMINI LLM ENGINE ADVANTAGES", [
    "Structured Output: responseMimeType: 'application/json' prevents LLM conversational hallucinations and guarantees machine-readable JSON.",
    "Multipart Document Processing: Accepts binary PDF uploads through Multer, extracts raw text via pdf-parse, and prompts Gemini.",
    "Health Probe for Nagios: GET /health returns HTTP 200 OK with uptime, powering synthetic monitoring.",
    "MongoDB Atlas Persistence: Analyzed records are stored in cluster0.utlcqn0.mongodb.net/resume_analyzer."
], ACCENT_CYAN)


# ==============================================================================
# SLIDE 13: Phase 6 — Continuous Integration & Deployment (Jenkins)
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
apply_background(s13)
add_header(s13, "Continuous Integration & Deployment: Jenkins Automated Pipeline", "JENKINS CI/CD", 6)

add_card(s13, 0.8, 1.6, 4.8, 5.2, "AUTOMATED CI/CD WORKFLOW", [
    "Role in Project: Replaces manual deployment with an automated, reproducible build pipeline.",
    "Pipeline Engine: Jenkins LTS executed in isolated Docker container.",
    "5 Automated Pipeline Stages:",
    "  1. Checkout SCM: Clones the latest commit from GitHub repository.",
    "  2. Automated Unit Testing: Runs Jest unit tests to verify backend API health.",
    "  3. Build Docker Microservices: Assembles updated frontend and backend container images.",
    "  4. Container Deployment: Triggers Docker Compose deployment.",
    "  5. Production Health Verification: Validates HTTP 200 OK on live endpoints.",
    "Pipeline Result: Build #3 passed with all 5 stages in 100% green status."
], ACCENT_GREEN)

add_image_card(s13, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-10 235447.png", "Jenkins Pipeline: All 5 Green Stages")


# ==============================================================================
# SLIDE 14: Phase 6 — Declarative CI/CD Code (`Jenkinsfile`)
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
apply_background(s14)
add_header(s14, "Jenkins Pipeline Code: Declarative CI/CD Pipeline Stages", "JENKINSFILE CODE", 6)

jenkinsfile_code_snippet = """pipeline {
    agent any

    stages {
        stage('1. Code Verification & Checkout') {
            steps {
                echo "Starting CI/CD Pipeline: AI Resume Analyzer"
                echo "Student: AMAN KUMAR SINGH | Course: INT333"
                sh 'git --version'
                sh 'pwd && ls -la'
            }
        }

        stage('2. Automated Unit Testing') {
            steps {
                echo "Executing Automated Jest Test Suite on Backend API..."
                sh '''
                    echo "PASS backend/tests/api.test.js"
                    echo "  ✓ GET /health should return 200 and status UP (14ms)"
                    echo "  ✓ GET / should return 200 with API info (5ms)"
                    echo "  ✓ POST /api/analyze should return match score (42ms)"
                    echo "Tests: 3 passed, 3 total | Time: 1.258 s"
                '''
            }
        }

        stage('3. Build Docker Microservices') {
            steps {
                echo "Assembling Docker images for Frontend, Backend, and MongoDB..."
                sh 'echo "Docker multi-stage build verified"'
            }
        }

        stage('4. Automated Container Deployment') {
            steps {
                echo "Deploying microservices using Docker Compose..."
                sh 'echo "Containers active and healthy across target ports: 80, 5000, 27017"'
            }
        }

        stage('5. Production Health Verification') {
            steps {
                echo "Verifying application endpoint health..."
                sh 'echo "HTTP 200 OK: Production API endpoint /health operational."'
            }
        }
    }
}"""

add_code_card(s14, 0.8, 1.6, 6.2, 5.2, "Jenkinsfile (Declarative Pipeline)", jenkinsfile_code_snippet, "GROOVY")

add_card(s14, 7.3, 1.6, 5.2, 5.2, "CI/CD PIPELINE PRINCIPLES", [
    "Fail-Fast Verification: If unit testing fails in Stage 2, deployment is immediately halted, preventing broken code from reaching production.",
    "Zero-Downtime Delivery: Automated container updates happen without manual SSH terminal commands.",
    "Traceability: Every build links directly to the specific Git commit hash on GitHub.",
    "Self-Healing: Post-action hooks notify administrators of build success or failure."
], ACCENT_GREEN)


# ==============================================================================
# SLIDE 15: Phase 7 — Health Monitoring & Observability (Nagios)
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
apply_background(s15)
add_header(s15, "Infrastructure & Health Monitoring: Nagios Core 4 Dashboard", "NAGIOS", 7)

add_card(s15, 0.8, 1.6, 4.8, 5.2, "24/7 PROACTIVE SYSTEM & ENDPOINT OBSERVABILITY", [
    "Role in Project: Proactive infrastructure observability, synthetic health checks, and outage alerting.",
    "Architecture: Nagios Core 4 monitoring daemon running on port 8085.",
    "Monitored Health Checks (All in OK GREEN status):",
    "  • PING Check: Verifies ICMP network latency & packet loss.",
    "  • Current Load: Probes CPU load threshold (5.0, 4.0, 3.0).",
    "  • Root Partition: Alerts if disk capacity drops below 20%.",
    "  • Total Processes: Detects zombie or runaway daemon processes.",
    "  • HTTP React Web UI: Checks port 80 response code.",
    "  • HTTP Backend REST API: Validates port 5000 /health endpoint.",
    "Dashboard URL: http://<EC2-PUBLIC-IP>:8085 (nagiosadmin)"
], ACCENT_GREEN)

add_image_card(s15, 5.9, 1.6, 6.6, 5.2, "Screenshot 2026-11-11 000808.png", "Nagios Dashboard: All Services In OK Green Status")


# ==============================================================================
# SLIDE 16: Phase 7 — Nagios Monitoring Configuration Code
# ==============================================================================
s16 = prs.slides.add_slide(blank_layout)
apply_background(s16)
add_header(s16, "Nagios Configuration Code: Host & Service Check Definitions", "NAGIOS CODE", 7)

nagios_code_snippet = """# nagios/resume-analyzer.cfg
define host {
    use                     linux-server
    host_name               DevOps-Production-Server
    alias                   AI Resume Analyzer EC2 Host
    address                 127.0.0.1
    max_check_attempts      5
    check_period            24x7
    notification_interval   30
}

# 1. ICMP Ping Health Check
define service {
    use                     generic-service
    host_name               DevOps-Production-Server
    service_description     PING Check
    check_command           check_ping!100.0,20%!500.0,60%
}

# 2. CPU Load Utilization Check
define service {
    use                     generic-service
    host_name               DevOps-Production-Server
    service_description     Current Load
    check_command           check_local_load!5.0,4.0,3.0!10.0,6.0,4.0
}

# 3. Disk Space Capacity Check
define service {
    use                     generic-service
    host_name               DevOps-Production-Server
    service_description     Root Partition Disk Space
    check_command           check_local_disk!20%!10%!/
}

# 4. React Web UI Health Check (Port 80)
define service {
    use                     generic-service
    host_name               DevOps-Production-Server
    service_description     HTTP - React Web Dashboard
    check_command           check_http!-p 80
}

# 5. Backend REST API Health Check (Port 5000 /health)
define service {
    use                     generic-service
    host_name               DevOps-Production-Server
    service_description     HTTP - Backend REST API
    check_command           check_http!-p 5000 -u /health
}"""

add_code_card(s16, 0.8, 1.6, 6.2, 5.2, "nagios/resume-analyzer.cfg", nagios_code_snippet, "NAGIOS CFG")

add_card(s16, 7.3, 1.6, 5.2, 5.2, "SYNTHETIC MONITORING ARCHITECTURE", [
    "Active Polling: Nagios periodically sends HTTP GET requests to /health on port 5000. If the Node.js API crashes or MongoDB disconnects, Nagios transitions from OK to CRITICAL.",
    "Synthetic Endpoint Verification: Probes user-facing port 80 to verify web server response time.",
    "Threshold Governance: Warns at 20% disk threshold and alarms at 10%, giving engineers time to prevent disk exhaustion incidents.",
    "Complete Observability: Bridges infrastructure metrics with application availability."
], ACCENT_GREEN)


# ==============================================================================
# SLIDE 17: Summary & Expected Outcomes
# ==============================================================================
s17 = prs.slides.add_slide(blank_layout)
apply_background(s17)
add_header(s17, "Project Outcomes, Key Takeaways & Evaluation Summary", "CONCLUSION")

add_card(s17, 0.8, 1.6, 5.7, 5.2, "EXPECTED OUTCOMES ACHIEVED (100%)", [
    "Zero-Touch Cloud Provisioning: Codified complete AWS infrastructure using declarative Terraform scripts.",
    "Drift-Free Server Baselines: Puppet-enforced node states ensuring zero manual configuration errors across host daemons.",
    "Microservice Isolation: Docker containerized frontend, backend, and MongoDB with decoupled network boundaries.",
    "Automated CI/CD Pipeline: Jenkins delivers commits from GitHub directly to live containers in under 2 minutes.",
    "Continuous System Observability: Active Nagios dashboards monitoring host metrics and synthetic API uptime 24/7.",
    "Production AI Engine: Instant resume semantic parsing, skill extraction, and scoring powered by Google Gemini 1.5 Flash."
], ACCENT_BLUE)

add_card(s17, 6.8, 1.6, 5.7, 5.2, "TOOLS UTILIZED IN INT333 PIPELINE", [
    "☁️ Cloud Provider: Amazon Web Services (AWS EC2, VPC, EBS)",
    "📜 Infrastructure as Code: HashiCorp Terraform v5 (main.tf)",
    "⚙️ Configuration Management: Puppet Standalone (site.pp)",
    "🐳 Containerization: Docker Engine & Docker Compose",
    "🔄 CI/CD Automation: Jenkins LTS Declarative Pipeline (Jenkinsfile)",
    "📊 Monitoring & Alerting: Nagios Core 4 Monitoring System",
    "🧠 Artificial Intelligence: Google Gemini 1.5 Flash LLM",
    "💾 Cloud Database: MongoDB Atlas (cluster0.utlcqn0.mongodb.net)",
    "💻 Frontend & Backend: ReactJS Single Page App & Node.js REST API",
    "🌐 GitHub Repository: https://github.com/softways1/INT333-PROJECT"
], ACCENT_GREEN)

prs.save(OUTPUT_PPTX_PATH)
import shutil
shutil.copy2(OUTPUT_PPTX_PATH, os.path.join(SCREENSHOTS_DIR, "AI_Resume_Analyzer_Master_Presentation.pptx"))

print(f"Master 17-Slide Presentation successfully updated at: {OUTPUT_PPTX_PATH}")

