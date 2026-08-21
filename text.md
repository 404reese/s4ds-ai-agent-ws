Yep — you want **raw Markdown**, so you can paste it directly into `README.md`.


# Resume + Job Description Demo Data

This section contains a deliberately imperfect **Job Description (JD)** and **Resume** that can be used to test a resume optimization / ATS agent.

The goal is to compare the **input** and **optimized output** and verify whether the agent can identify missing keywords, improve bullet points, and better align the resume with the JD.

---

## Input JD
```markdown
# Software Engineer — Backend

**Company:** FinTech Labs  
**Location:** Mumbai / Hybrid  
**Experience:** 2–4 years

We are looking for a Software Engineer to join our backend engineering team.

### Responsibilities

- Develop and maintain backend services and REST APIs.
- Build scalable and reliable applications.
- Work with databases and improve query performance.
- Write unit and integration tests.
- Debug production issues and improve system reliability.
- Collaborate with frontend engineers, product managers, and QA.
- Participate in code reviews and technical discussions.

### Requirements

- 2+ years of software development experience.
- Strong experience with Python.
- Experience with Django or FastAPI.
- Good understanding of REST APIs and microservices.
- Experience with PostgreSQL or similar relational databases.
- Familiarity with AWS, Docker, and CI/CD.
- Strong problem-solving and communication skills.

### Nice to Have

- Experience with Redis or Kafka.
- Knowledge of payment or fintech systems.
- Experience with monitoring and observability tools.


```

## Input Resume
```markdown
# Rahul Mehta

Mumbai, India

rahul.mehta@example.com | +91 98765 43210

## Summary

Software developer with around 3 years of experience working on web applications. Have worked on backend and frontend development using different technologies. Looking for opportunities to grow and work on challenging projects.

## Skills

Python, JavaScript, React, Node.js, Django, PostgreSQL, MySQL, Git, Docker, AWS, HTML, CSS, REST APIs

## Experience

### Software Developer — WebSolutions Pvt. Ltd.

**Mumbai | 2023 – Present**

- Worked on web applications using Python and Django.
- Developed APIs for different application features.
- Worked with PostgreSQL and wrote SQL queries.
- Fixed bugs reported by customers and QA.
- Worked with frontend developers to integrate APIs.
- Used Git for version control.
- Helped deploy applications on AWS.
- Participated in daily standups and sprint planning.

### Junior Developer — AppWorks

**Pune | 2022 – 2023**

- Developed features for a web application.
- Worked with JavaScript, React and Node.js.
- Created some backend APIs.
- Fixed bugs and improved existing functionality.
- Worked with databases.
- Participated in code reviews.

## Projects

### Online Shopping Application

Built an e-commerce application using React, Node.js and MongoDB. Implemented login, product listing, shopping cart and checkout functionality.

### Employee Management System

Created a web application using Python and Django to manage employee records.

## Education

**B.E. Computer Engineering**  
ABC Institute of Technology  
2018 – 2022

## Certifications

- AWS Cloud Practitioner
- Python Programming Certificate

---

## Purpose of This Dataset

This demo input is intentionally not fully optimized for the target role.

An AI resume optimization agent should ideally identify opportunities such as:

- Better alignment with the backend Software Engineer role.
- Stronger emphasis on Python and Django.
- Highlighting REST API development.
- Highlighting PostgreSQL and database work.
- Highlighting AWS and Docker experience.
- Adding relevant testing experience where truthful.
- Improving weak and generic experience bullets.
- Making backend experience more prominent than frontend experience.
- Identifying missing or weak JD keywords.
- Improving the professional summary.
- Quantifying achievements where the candidate has legitimate metrics.
- Avoiding fabricated experience or technologies.

The optimized resume should remain truthful to the original candidate information.
```
