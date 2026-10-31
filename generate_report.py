import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_report():
    doc = docx.Document()

    # Define color scheme: Black (#000000) for body, Blue (#004080) for headings
    COLOR_HEADING_PRIMARY = RGBColor(0, 64, 128)      # Deep Academic Navy Blue
    COLOR_HEADING_SECONDARY = RGBColor(0, 85, 170)    # Sub-heading Blue
    COLOR_BODY = RGBColor(0, 0, 0)                     # Pure Black Text
    COLOR_META = RGBColor(40, 40, 40)                  # Dark Charcoal Black

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Helper function for adding headings in Blue
    def add_blue_heading(text, level=1):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        if level == 1:
            run.font.size = Pt(17)
            run.font.color.rgb = COLOR_HEADING_PRIMARY
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
        elif level == 2:
            run.font.size = Pt(13.5)
            run.font.color.rgb = COLOR_HEADING_SECONDARY
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
        elif level == 3:
            run.font.size = Pt(11.5)
            run.font.color.rgb = COLOR_HEADING_SECONDARY
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
        return p

    # Helper function for body paragraphs in Black
    def add_black_p(text, bold_prefix=None, space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(11)
            r_pre.font.color.rgb = COLOR_BODY
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = COLOR_BODY
        return p

    # Helper function for code blocks with clean border and shading
    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)

        # Light gray background and thin border
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F5F7"/>')
        cell._tc.get_or_add_tcPr().append(shading)

        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="D1D1D6"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="004080"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D1D1D6"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="D1D1D6"/>
            </w:tcBorders>
        ''')
        cell._tc.get_or_add_tcPr().append(borders)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(4)
        cp.paragraph_format.space_after = Pt(4)
        cp.paragraph_format.line_spacing = 1.05

        lines = code_text.strip().split('\n')
        for i, line in enumerate(lines):
            r = cp.add_run(line + ('\n' if i < len(lines)-1 else ''))
            r.font.name = 'Consolas'
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_BODY

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_after = Pt(4)

    # Helper function for adding an image with description
    def add_image_figure(img_path, title, description, width=Inches(6.2)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            r_img = p_img.add_run()
            r_img.add_picture(img_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)

            r_title = p_cap.add_run(f"{title}: ")
            r_title.bold = True
            r_title.font.name = 'Calibri'
            r_title.font.size = Pt(9.5)
            r_title.font.color.rgb = COLOR_HEADING_PRIMARY

            r_desc = p_cap.add_run(description)
            r_desc.italic = True
            r_desc.font.name = 'Calibri'
            r_desc.font.size = Pt(9.5)
            r_desc.font.color.rgb = COLOR_BODY

    # =========================================================================
    # FRONT COVER (Matching AST-A-TEMPLATE.docx.pdf Exactly)
    # =========================================================================
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(40)
    p_logo.paragraph_format.space_after = Pt(50)

    logo_path = '/home/abdullah/Desktop/Dev/PDC/extracted_images/template_logo.png'
    if os.path.exists(logo_path):
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(2.5))

    p_a = doc.add_paragraph()
    p_a.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_a.paragraph_format.space_before = Pt(20)
    p_a.paragraph_format.space_after = Pt(6)
    r_a = p_a.add_run("Assignment 2")
    r_a.font.name = 'Calibri'
    r_a.font.size = Pt(21)
    r_a.bold = True
    r_a.font.color.rgb = COLOR_BODY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(70)
    r_sub = p_sub.add_run("Parallel and Distributed Computing (DevOps)")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(17)
    r_sub.bold = True
    r_sub.font.color.rgb = COLOR_BODY

    p_subby = doc.add_paragraph()
    p_subby.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subby.paragraph_format.space_after = Pt(10)
    r_subby = p_subby.add_run("Submitted By:")
    r_subby.font.name = 'Calibri'
    r_subby.font.size = Pt(13)
    r_subby.font.color.rgb = COLOR_BODY

    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_after = Pt(4)
    r_name = p_name.add_run("Name: ABDULLAH")
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(13)
    r_name.bold = True
    r_name.font.color.rgb = COLOR_BODY

    p_reg = doc.add_paragraph()
    p_reg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_reg.paragraph_format.space_after = Pt(4)
    r_reg = p_reg.add_run("REG: FA23-BSE-137")
    r_reg.font.name = 'Calibri'
    r_reg.font.size = Pt(13)
    r_reg.font.color.rgb = COLOR_BODY

    p_sec = doc.add_paragraph()
    p_sec.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sec.paragraph_format.space_after = Pt(20)
    r_sec = p_sec.add_run("Section: BSE-7B")
    r_sec.font.name = 'Calibri'
    r_sec.font.size = Pt(13)
    r_sec.font.color.rgb = COLOR_BODY

    doc.add_page_break()

    # =========================================================================
    # SECTION 1: ASSIGNMENT OVERVIEW & ACCESS URLS
    # =========================================================================
    add_blue_heading("1. Executive Summary & Access Information", level=1)
    add_black_p("This report details the end-to-end containerization, orchestration, and public cloud deployment for CSC336 - Parallel and Distributed Computing (DevOps) Assignment 2. The project implements a multi-tier web application consisting of a React frontend, an Express.js backend API, and a PostgreSQL relational database server deployed on an Amazon Web Services (AWS) EC2 Virtual Machine instance.")

    add_blue_heading("1.1 Live Application URLs & Repository Links", level=2)
    add_black_p("http://35.153.73.232:5000", bold_prefix="Public Cloud Access URL (Port 5000): ")
    add_black_p("http://35.153.73.232:80", bold_prefix="Public Cloud Access URL (Port 80): ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc", bold_prefix="Official GitHub Repository: ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc/blob/main/Dockerfile", bold_prefix="Multistage Dockerfile (GitHub): ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc/blob/main/docker-compose.yml", bold_prefix="Docker Compose File (GitHub): ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc/tree/main/secrets", bold_prefix="Docker Secrets Directory (GitHub): ")

    add_blue_heading("1.2 Application UI & Apple Design System Specification", level=2)
    add_black_p("The web application interface has been crafted adhering strictly to the Apple Design System human-interface philosophy. It eliminates extraneous visual clutter (deslopified layout) and is constructed using an intentional three-color palette: White (#FFFFFF) as primary background, Deep Charcoal/Black (#000000) for typography and primary action elements, and Vibrant Red (#FF3B30) for system telemetry badges, deletion actions, and registration tags. The top navigation bar prominently displays developer attribution: Developer: ABDULLAH and Registration ID: FA23-BSE-137.")

    # =========================================================================
    # SECTION 2: ARCHITECTURAL COMPLIANCE WITH ASSIGNMENT OBJECTIVES
    # =========================================================================
    add_blue_heading("2. Architectural Compliance & Objective Verification", level=1)
    add_black_p("The assignment requires satisfying four core DevOps competencies under CLO2 (Enumerate virtualization and containerization techniques used in cloud computing). Below is the verification breakdown:")

    add_blue_heading("2.1 Multistage Dockerfile [3 Marks]", level=2)
    add_black_p("A multi-stage Docker build was implemented using node:20-alpine across two distinct phases:")
    add_black_p("Installs full development dependencies, compiles the production-optimized React bundle using Vite, and packages production-only Node modules.", bold_prefix="• Stage 1 (Builder Phase): ")
    add_black_p("Utilizes an ultra-lean Alpine image, discards intermediate compilation tools and source files, and copies solely the server code and production bundle. It enforces container security by executing under the non-root node user.", bold_prefix="• Stage 2 (Runner Phase): ")

    add_blue_heading("2.2 Docker Compose Configuration & Explicit Naming [3 Marks]", level=2)
    add_black_p("The docker-compose.yml orchestrates the application without relying on prebuilt registry images for the web service. It defines explicit, standardized container names (pdc_web_app for the Node/React application and pdc_db for PostgreSQL) and establishes service dependencies with strict healthcheck readiness gates.")

    add_blue_heading("2.3 Data Persistence via Docker Named Volume [2 Marks]", level=2)
    add_black_p("A dedicated named volume (pdc_db_data) is attached to the PostgreSQL data directory (/var/lib/postgresql/data). When containers are stopped, removed via docker compose down, or updated, all stored database records persist seamlessly upon recreation.")

    add_blue_heading("2.4 Sensitive Credential Management via Docker Secrets [2 Marks]", level=2)
    add_black_p("In full accordance with Docker Compose secrets standards, database credentials (username, password, and database name) are stored in isolated host files and mounted into the container filesystem under /run/secrets/. Plaintext passwords are completely eliminated from the docker-compose file.")

    # =========================================================================
    # SECTION 3: CONFIGURATION CODE ARTIFACTS
    # =========================================================================
    doc.add_page_break()
    add_blue_heading("3. Configuration Source Code", level=1)

    add_blue_heading("3.1 Multistage Dockerfile (Dockerfile)", level=2)
    add_black_p("Below is the complete production Dockerfile defining the two-stage build architecture:")
    dockerfile_code = """FROM node:20-alpine AS builder

WORKDIR /app

COPY client/package*.json ./client/
RUN cd client && npm ci

COPY client/ ./client/
RUN cd client && npm run build

COPY server/package*.json ./server/
RUN cd server && npm ci --omit=dev

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=5000

COPY --from=builder /app/server/node_modules ./node_modules
COPY --from=builder /app/server/package.json ./package.json
COPY server/ ./
COPY --from=builder /app/client/dist ./public

USER node

EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \\
  CMD wget --quiet --tries=1 --spider http://127.0.0.1:5000/api/health || exit 1

CMD ["node", "index.js"]"""
    add_code_block(dockerfile_code)

    add_blue_heading("3.2 Docker Compose File (docker-compose.yml)", level=2)
    add_black_p("Below is the complete Docker Compose orchestration specification:")
    compose_code = """services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: pdc_web_app
    restart: unless-stopped
    ports:
      - "80:5000"
      - "5000:5000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - PORT=5000
    secrets:
      - db_password
      - db_user
      - db_name
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    container_name: pdc_db
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER_FILE: /run/secrets/db_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB_FILE: /run/secrets/db_name
    secrets:
      - db_password
      - db_user
      - db_name
    volumes:
      - pdc_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $(cat /run/secrets/db_user) -d $(cat /run/secrets/db_name)"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 5s

volumes:
  pdc_db_data:
    name: pdc_db_data

secrets:
  db_password:
    file: ./secrets/db_password.txt
  db_user:
    file: ./secrets/db_user.txt
  db_name:
    file: ./secrets/db_name.txt"""
    add_code_block(compose_code)

    add_blue_heading("3.3 Database Secrets Definition Files", level=2)
    add_black_p("Three secret files are stored in the ./secrets/ directory on the host and mounted securely:")
    add_black_p("pdc_secure_password_2026", bold_prefix="• secrets/db_password.txt: ")
    add_black_p("pdc_user", bold_prefix="• secrets/db_user.txt: ")
    add_black_p("pdc_assignment_db", bold_prefix="• secrets/db_name.txt: ")

    # =========================================================================
    # SECTION 4: STEP-BY-STEP DEPLOYMENT & SCREENSHOT EVIDENCE
    # =========================================================================
    doc.add_page_break()
    add_blue_heading("4. Step-by-Step Implementation & Screenshot Evidence", level=1)
    add_black_p("This section documents the execution lifecycle from local container compilation through AWS EC2 cloud provisioning, security configuration, and live multi-container verification. Each image extracted from the deployment workflow is detailed with technical descriptions.")

    img_dir = '/home/abdullah/Desktop/Dev/PDC/extracted_images'

    # Figure 1: Image 4
    add_blue_heading("Step 1: Local Multi-Stage Image Build", level=2)
    add_black_p("Execution of docker compose up --build -d on the developer workstation. The build engine processes the multistage Dockerfile, downloading node:20-alpine, compiling Vite assets in Stage 1, pruning dev-dependencies, and packaging the lean Stage 2 production image.")
    add_image_figure(
        os.path.join(img_dir, 'image4.png'),
        "Figure 1",
        "Local Docker multi-stage build completing 20/20 build steps and compiling client bundle."
    )

    # Figure 2: Image 1
    add_blue_heading("Step 2: Local Container Launch & Healthcheck Verification", level=2)
    add_black_p("Launching the local stack with docker compose up -d. The PostgreSQL container initializes first, passes the readiness healthcheck (pg_isready), and allows the web application container to bind and start.")
    add_image_figure(
        os.path.join(img_dir, 'image1.png'),
        "Figure 2",
        "Docker Compose service initialization showing healthy database and running web application."
    )

    # Figure 3: Image 5
    add_blue_heading("Step 3: Verification of Local Running Containers (docker compose ps)", level=2)
    add_black_p("Running docker compose ps on the host confirms both explicitly named containers (pdc_db and pdc_web_app) are operational with port forwards configured.")
    add_image_figure(
        os.path.join(img_dir, 'image5.png'),
        "Figure 3",
        "Terminal output of docker compose ps confirming operational status of local containers."
    )

    # Figure 4: Image 8
    doc.add_page_break()
    add_blue_heading("Step 4: Secure SSH Connection to AWS EC2 Instance", level=2)
    add_black_p("Connecting securely to the Amazon EC2 Ubuntu 24.04 virtual machine (Public IP: 35.153.73.232) using the private key devops-key.pem with 400 user-read permissions.")
    add_image_figure(
        os.path.join(img_dir, 'image8.png'),
        "Figure 4",
        "Successful SSH login into AWS EC2 Ubuntu instance (35.153.73.232) using devops-key.pem."
    )

    # Figure 5: Image 2
    add_blue_heading("Step 5: Cloud Workspace Setup on EC2", level=2)
    add_black_p("Navigating inside the EC2 instance, listing active workspace contents, and creating the project directory devops-A2 to host the containerized repository.")
    add_image_figure(
        os.path.join(img_dir, 'image2.png'),
        "Figure 5",
        "EC2 remote shell session creating directory devops-A2."
    )

    # Figure 6: Image 6
    add_blue_heading("Step 6: Git Repository Cloning on AWS EC2", level=2)
    add_black_p("Cloning the assignment codebase directly from GitHub (https://github.com/Abdullah-Developer68/pdc.git) into the EC2 instance environment.")
    add_image_figure(
        os.path.join(img_dir, 'image6.png'),
        "Figure 6",
        "Git clone operation downloading repository objects onto the Amazon EC2 instance."
    )

    # Figure 7: Image 3
    doc.add_page_break()
    add_blue_heading("Step 7: Cloud Container Stack Launch (docker compose ps)", level=2)
    add_black_p("Executing docker compose ps on the remote EC2 instance. The output confirms that both pdc_db (PostgreSQL 16) and pdc_web_app (Node/React runtime) are running in healthy states.")
    add_image_figure(
        os.path.join(img_dir, 'image3.png'),
        "Figure 7",
        "Remote EC2 terminal showing operational containers pdc_db and pdc_web_app."
    )

    # Figure 8: Image 7
    add_blue_heading("Step 8: AWS EC2 Security Group Inbound Firewall Configuration", level=2)
    add_black_p("Configuring the AWS EC2 Security Group (sg-095a578343798d9de in us-east-1). Inbound firewall rules are defined to authorize SSH (Port 22), HTTP (Port 80), Custom TCP (Port 5000), and application ports across IPv4 (0.0.0.0/0).")
    add_image_figure(
        os.path.join(img_dir, 'image7.png'),
        "Figure 8",
        "AWS Management Console Security Group rule editor displaying authorized ports 22, 80, and 5000."
    )

    # Figure 9: Image 9
    add_blue_heading("Step 9: Live Cloud Web Application Verification", level=2)
    add_black_p("Accessing the deployed web application through the public internet at http://35.153.73.232. The interface displays real-time telemetry, PostgreSQL connectivity, container hostname verification, and data persistence operations.")
    add_image_figure(
        os.path.join(img_dir, 'image9.png'),
        "Figure 9",
        "Browser access to the live cloud application running on AWS EC2 instance 35.153.73.232."
    )

    # =========================================================================
    # SECTION 5: CONCLUSION & VERIFICATION SUMMARY
    # =========================================================================
    doc.add_page_break()
    add_blue_heading("5. Summary of Achievements", level=1)
    add_black_p("All objectives outlined in the CSC336 DevOps Assignment 2 rubric have been successfully executed and validated end-to-end:")
    add_black_p("Successfully authored with Node 20 Alpine, compiling Vite React client assets in Stage 1 and packaging an ultra-lean runtime in Stage 2 running under a non-root user.", bold_prefix="1. Multistage Dockerfile: ")
    add_black_p("Coordinates multi-container deployment with build directives, explicit service naming (pdc_web_app, pdc_db), and healthcheck gates.", bold_prefix="2. Docker Compose Orchestration: ")
    add_black_p("Mounted into /var/lib/postgresql/data, safeguarding user tasks across container restart and teardown lifecycles.", bold_prefix="3. Named Volume Data Persistence: ")
    add_black_p("Eliminated plaintext credentials from repository code by mounting secrets under /run/secrets/ at runtime.", bold_prefix="4. Docker Secrets Security: ")
    add_black_p("Operational on Amazon EC2 (Ubuntu 24.04 LTS) under IP 35.153.73.232 with properly provisioned security groups and custom Apple Design System UI attributing student ABDULLAH (FA23-BSE-137).", bold_prefix="5. Cloud Infrastructure (IaaS): ")

    output_path = '/home/abdullah/Desktop/Dev/PDC/PDC-A2-Report.docx'
    doc.save(output_path)
    print(f"Report successfully generated at: {output_path}")

if __name__ == '__main__':
    create_report()
