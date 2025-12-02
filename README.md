## Future Academy Education Management (Odoo 15)

This repository contains my graduation project: an **education management system** built on **Odoo 15**.  
It digitizes core processes of an educational institute such as admissions, student records, attendance, classrooms, and timetables. **[View Project Presentation](https://sevenpic.my.canva.site/technology-in-education-technology-presentation)** – Technology in Education presentation showcasing the project overview and features.

### Features

- **Core (`core`)**: Students, faculties, departments, courses, batches, academic years/terms, projects, and student portal.
- **Admissions (`admission`)**: Admission registers, application workflow, eligibility checks (age, dates), and automatic student creation.
- **Attendance (`attendance`)**: Attendance registers and sheets, per-session student attendance, and reports.
- **Timetable (`timetable`)**: Sessions with classroom, subject, faculty, and batch; timetable conflict checks; notifications to students/faculty.
- **Classrooms (`classroom`)**: Classroom definitions used by the timetable and sessions.

> Note: The modules `sh_entmate_theme` and `sh_ent_theme_config` are **commercial themes** from Softhealer.  
> They are present in my local development environment but should not be redistributed without a valid license.

### Tech Stack

- **Platform**: Odoo 15 (Python, PostgreSQL)
- **Backend**: Odoo ORM models, business logic in Python
- **Frontend**: Odoo views, QWeb, and (optionally) commercial backend theme

### How to Run

1. Install **Odoo 15** and configure a PostgreSQL database.
2. Clone this repository into an addons directory accessible by Odoo:
   - Example: `H:\odoo\custom_addons\future_academy` on Windows, or `/opt/odoo/custom_addons/future_academy` on Linux.
3. Add the path to your Odoo configuration (`addons_path`) and restart the Odoo server.
4. In Odoo:
   - Activate Developer Mode.
   - Install the modules in this order (at minimum):
     - `core`
     - `classroom`
     - `admission`
     - `attendance`
     - `timetable`
5. Configure:
   - Academic years, terms, courses, and batches.
   - Admission registers and minimum age criteria.
   - Faculty and classroom data.

### Repository Structure

- `core/` – Core academic models (students, faculty, course structure, student portal, reports).
- `admission/` – Admission process, registers, and wizards.
- `attendance/` – Attendance sheets, registers, and reports.
- `timetable/` – Session scheduling and timetable constraints.
- `classroom/` – Classroom model and views.
- `sh_entmate_theme/`, `sh_ent_theme_config/` – **Third-party commercial themes** (not part of the open-source deliverable).

### License

All custom code in this repository (excluding third‑party modules like `sh_entmate_theme` and `sh_ent_theme_config`) is released by **Abdallah (`abdallahh166`)** under the **MIT License**.  
Third‑party modules remain subject to their original licenses and are **not** granted under MIT.


