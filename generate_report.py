import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_assignment_report():
    doc = docx.Document()

    COLOR_HEADING_PRIMARY = RGBColor(0, 64, 128)      # Blue (#004080)
    COLOR_HEADING_SECONDARY = RGBColor(0, 85, 170)    # Blue (#0055AA)
    COLOR_BODY = RGBColor(0, 0, 0)                     # Pure Black (#000000)

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    def add_blue_heading(text, level=1):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = COLOR_HEADING_PRIMARY
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = COLOR_HEADING_SECONDARY
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
        elif level == 3:
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_HEADING_SECONDARY
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
        return p

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

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)

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
    # FRONT COVER (Exact Uniform Font Style Matching AST Template)
    # =========================================================================
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(40)
    p_logo.paragraph_format.space_after = Pt(45)

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
    r_a.font.size = Pt(18)
    r_a.bold = True
    r_a.font.color.rgb = COLOR_BODY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(60)
    r_sub = p_sub.add_run("Parallel and Distributed Computing")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(18)
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
    # SECTION 1: OVERVIEW & REPOSITORY INFORMATION
    # =========================================================================
    add_blue_heading("1. Overview & Cloud Access Information", level=1)
    add_black_p("This report presents the containerization, orchestration, and public cloud deployment for CSC336 - Parallel and Distributed Computing (DevOps) Assignment 2. The assignment requires deploying a containerized multi-tier web application consisting of a web application service and a database server on an Amazon Web Services (AWS) EC2 Virtual Machine instance.")

    add_blue_heading("1.1 Live Application URLs & Repository Links", level=2)
    add_black_p("http://35.153.73.232:5000", bold_prefix="Public Cloud Access URL (Port 5000): ")
    add_black_p("http://35.153.73.232:80", bold_prefix="Public Cloud Access URL (Port 80): ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc", bold_prefix="Official GitHub Repository: ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc/blob/main/Dockerfile", bold_prefix="Multistage Dockerfile (GitHub Link): ")
    add_black_p("https://github.com/Abdullah-Developer68/pdc/blob/main/docker-compose.yml", bold_prefix="Docker Compose File (GitHub Link): ")

    # =========================================================================
    # SECTION 2: OBJECTIVES & REQUIREMENTS
    # =========================================================================
    add_blue_heading("2. Fulfillment of Assignment Objectives", level=1)
    add_black_p("The deployment satisfies all containerization and cloud computing requirements specified in the assignment:")
    add_black_p("A two-stage Dockerfile was authored. Stage 1 (Build stage) installs dependencies and compiles the application bundle. Stage 2 (Runtime stage) utilizes a lightweight Alpine Linux base image, copying only compiled artifacts to minimize image size and running as a non-root user.", bold_prefix="• Multistage Dockerfile: ")
    add_black_p("A docker-compose.yml file defines and launches the web application and database services. The web application service is configured to build directly from the Dockerfile rather than using a prebuilt image.", bold_prefix="• Docker Compose Orchestration: ")
    add_black_p("Both services explicitly specify container names: pdc_web_app for the web application and pdc_db for the database service.", bold_prefix="• Explicit Container Naming: ")
    add_black_p("A dedicated named volume (pdc_db_data) is attached to the database container at /var/lib/postgresql/data, ensuring that stored records remain intact when containers are recreated.", bold_prefix="• Named Volume Persistence: ")
    add_black_p("Sensitive credentials are managed via Docker Compose secrets mounted at /run/secrets/ inside the containers. Rather than hardcoding passwords in Compose, Docker mounts separate secret files securely at runtime.", bold_prefix="• Docker Secrets Management: ")
    add_black_p("The multi-container stack is deployed and running live on an Amazon EC2 instance (Ubuntu 24.04 LTS, Public IP: 35.153.73.232) under AWS IaaS.", bold_prefix="• AWS EC2 Cloud Deployment: ")

    # =========================================================================
    # SECTION 3: CODE IMPLEMENTATIONS & DOCKER SECRETS
    # =========================================================================
    doc.add_page_break()
    add_blue_heading("3. Configuration Files & Docker Secrets", level=1)

    add_blue_heading("3.1 Multistage Dockerfile (Dockerfile)", level=2)
    add_black_p("The multistage Dockerfile defines two distinct phases to optimize image size and enforce runtime security:")
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
    add_black_p("The docker-compose.yml defines multi-container coordination, port forwards, health checks, secrets, and the named volume:")
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

    add_blue_heading("3.3 Docker Secrets Files & Configuration", level=2)
    add_black_p("To avoid hardcoding sensitive database credentials in the Compose file or environment variables, Docker Compose secrets are utilized. Three distinct secret files are configured on the host filesystem under ./secrets/ and mounted as in-memory files at /run/secrets/ inside the containers:")

    add_black_p("The password used by PostgreSQL and the application backend.", bold_prefix="1. db_password (File: ./secrets/db_password.txt): ")
    add_code_block("pdc_secure_password_2026")

    add_black_p("The database user account authorized for connection pooling.", bold_prefix="2. db_user (File: ./secrets/db_user.txt): ")
    add_code_block("pdc_user")

    add_black_p("The database name initialized in PostgreSQL.", bold_prefix="3. db_name (File: ./secrets/db_name.txt): ")
    add_code_block("pdc_assignment_db")

    add_black_p("PostgreSQL natively reads these secrets at container initialization via the environment variables POSTGRES_PASSWORD_FILE, POSTGRES_USER_FILE, and POSTGRES_DB_FILE, guaranteeing that database credentials remain fully protected.")

    # =========================================================================
    # SECTION 4: STEP-BY-STEP DEPLOYMENT & SCREENSHOT EVIDENCE
    # =========================================================================
    doc.add_page_break()
    add_blue_heading("4. Step-by-Step Deployment & Screenshot Evidence", level=1)
    add_black_p("This section documents the sequential steps followed to containerize, verify, and deploy the application on AWS EC2, with detailed descriptions for each screenshot evidence.")

    img_dir = '/home/abdullah/Desktop/Dev/PDC/extracted_images'

    add_blue_heading("Step 1: Local Multistage Container Build", level=2)
    add_black_p("Executing docker compose up --build -d to construct the image using the multistage Dockerfile. The builder stage installs dependencies and builds the application bundle, while the final runtime image is constructed using a minimal alpine layer.")
    add_image_figure(
        os.path.join(img_dir, 'image4.png'),
        "Figure 1",
        "Multistage Docker build process executing on the local machine."
    )

    add_blue_heading("Step 2: Local Container Launch & Healthcheck Verification", level=2)
    add_black_p("Docker Compose launches both the database and web application services. The database container undergoes automated healthchecks before the web application container is started.")
    add_image_figure(
        os.path.join(img_dir, 'image1.png'),
        "Figure 2",
        "Starting the container stack with Docker Compose and verifying service readiness."
    )

    add_blue_heading("Step 3: Verification of Running Local Containers", level=2)
    add_black_p("Running docker compose ps on the host confirms both containers (pdc_db and pdc_web_app) are running with their designated container names and port allocations.")
    add_image_figure(
        os.path.join(img_dir, 'image5.png'),
        "Figure 3",
        "Verification of active local containers using docker compose ps."
    )

    doc.add_page_break()
    add_blue_heading("Step 4: Connecting to AWS EC2 Instance via SSH", level=2)
    add_black_p("Connecting to the Amazon EC2 instance (Ubuntu 24.04 LTS, Public IP: 35.153.73.232) via SSH using the private key devops-key.pem with appropriate 400 permissions.")
    add_image_figure(
        os.path.join(img_dir, 'image8.png'),
        "Figure 4",
        "Terminal session connecting to AWS EC2 instance 35.153.73.232 over SSH."
    )

    add_blue_heading("Step 5: Preparing Cloud Deployment Directory", level=2)
    add_black_p("Setting up the deployment directory devops-A2 on the EC2 instance to house the containerized application repository.")
    add_image_figure(
        os.path.join(img_dir, 'image2.png'),
        "Figure 5",
        "Directory initialization on the remote AWS EC2 instance."
    )

    add_blue_heading("Step 6: Cloning Project Codebase onto AWS EC2", level=2)
    add_black_p("Cloning the project repository from GitHub (https://github.com/Abdullah-Developer68/pdc.git) directly into the EC2 instance.")
    add_image_figure(
        os.path.join(img_dir, 'image6.png'),
        "Figure 6",
        "Cloning the application repository from GitHub onto the EC2 virtual machine."
    )

    doc.add_page_break()
    add_blue_heading("Step 7: Launching Multi-Container Stack on AWS EC2", level=2)
    add_black_p("Executing docker compose ps on the remote EC2 instance. The output confirms both the database (pdc_db) and web application (pdc_web_app) containers are operational and healthy.")
    add_image_figure(
        os.path.join(img_dir, 'image3.png'),
        "Figure 7",
        "Remote EC2 terminal showing operational status of pdc_db and pdc_web_app containers."
    )

    add_blue_heading("Step 8: Configuring AWS EC2 Security Group Inbound Rules", level=2)
    add_black_p("Configuring the AWS EC2 Security Group (sg-095a578343798d9de in us-east-1). Inbound firewall rules are authorized for SSH (Port 22), HTTP (Port 80), and Custom TCP (Port 5000) from anywhere (0.0.0.0/0).")
    add_image_figure(
        os.path.join(img_dir, 'image7.png'),
        "Figure 8",
        "AWS EC2 Management Console Security Group rule editor displaying authorized ports 22, 80, and 5000."
    )

    add_blue_heading("Step 9: Accessing Containerized Web Application on AWS EC2", level=2)
    add_black_p("Accessing the live deployed web application in the browser at http://35.153.73.232. The interface confirms live database connectivity, container hostname verification, and data persistence.")
    add_image_figure(
        os.path.join(img_dir, 'image9.png'),
        "Figure 9",
        "Browser view of the live containerized web application running on Amazon EC2 (35.153.73.232)."
    )

    # =========================================================================
    # SECTION 5: CONCLUSION
    # =========================================================================
    doc.add_page_break()
    add_blue_heading("5. Conclusion", level=1)
    add_black_p("All objectives of Assignment 2 have been successfully accomplished:")
    add_black_p("A two-stage build was created using Node 20 Alpine, minimizing the production runtime footprint.", bold_prefix="1. Multistage Dockerfile: ")
    add_black_p("Built the web application from source with explicit container names (pdc_web_app and pdc_db).", bold_prefix="2. Docker Compose: ")
    add_black_p("Configured pdc_db_data to safeguard data persistence across container restarts.", bold_prefix="3. Named Volume: ")
    add_black_p("Isolated credentials into Docker Compose secrets mounted at /run/secrets/.", bold_prefix="4. Docker Secrets: ")
    add_black_p("Successfully deployed and validated on AWS EC2 (Public IP: 35.153.73.232).", bold_prefix="5. Cloud Deployment: ")

    # Save files with standardized student naming
    output_docx = '/home/abdullah/Desktop/Dev/PDC/PDC-A2-FA23-BSE-137.docx'
    doc.save(output_docx)
    print(f"DOCX report saved at: {output_docx}")

    # Also keep PDC-A2-Report.docx updated
    doc.save('/home/abdullah/Desktop/Dev/PDC/PDC-A2-Report.docx')

    # Convert to PDF using LibreOffice
    cmd = [
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        output_docx,
        '--outdir', '/home/abdullah/Desktop/Dev/PDC'
    ]
    subprocess.run(cmd, check=True)
    print("PDF report successfully converted!")

if __name__ == '__main__':
    generate_assignment_report()
