# Vaquero Meets

Vaquero Meets is a Django-based social event application that allows users to create, discover, and interact with events based on shared interests. The app focuses on a modern, consistent user experience with smart filtering, RSVP tracking, comments, and event images.

**Current Branch:** `frontend-1`

---

## Features

### Event Management
- Create, edit, and view events
- Upload event images
- Set event details (date, time, location, capacity, visibility)
- Edit events only if you are the event owner

### Event Discovery
- Event list with modern glassmorphism UI
- Sort events by:
  - Soonest upcoming
  - Furthest future
  - Title (A–Z)
- Interest-based filtering with multi-select chips
- Smart default filtering based on user profile interests
- Clear filters without losing sort state

### RSVP System
- RSVP statuses: Going, Maybe, Not Going
- RSVP state updates per event
- Attendee list displayed on event detail page

### Comments
- Post comments on events
- Edit and delete your own comments
- Author-only permissions enforced

### Profiles
- User profiles with display name and interests
- Profile interest chips reused across the app
- Profile initials shown in navigation bar

### UI & UX
- Consistent navigation across all pages
- Glassmorphism design style
- Responsive layout using Bootstrap
- Subtle animations with GSAP

---

## Technologies Used

### Backend
- **Python**
- **Django**
- Django ORM (Object-Relational Mapper)

### Frontend
- **HTML**
- **CSS (custom glassmorphism styling)**
- **Bootstrap 5**
- **JavaScript**
- **GSAP (GreenSock Animation Platform)**

### Database
- **SQLite** (development database)

### Media Handling
- **Pillow** (image uploads)
- Django media file handling (`MEDIA_ROOT`, `MEDIA_URL`)

---

## Project Architecture

The application follows Django’s **Model–View–Template (MVT)** architecture:

- **Models**: Define database structure (Events, Interests, RSVPs, Comments, Profiles)
- **Views**: Handle application logic and user requests
- **Templates**: Render dynamic HTML pages
- **Forms**: Validate and process user input using Django Forms and ModelForms

---

## Authentication & Permissions

- Django’s built-in authentication system
- Login and logout functionality
- Permission checks ensure:
  - Only event owners can edit events
  - Only comment authors can edit or delete their comments
- CSRF protection enabled for all forms

---

## Admin Access (Development)

> ⚠️ **For development/testing only**

- **Admin URL:** `/admin/`
- **Username:** `admin`
- **Password:** `admin956`

---

## Running the Project Locally

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
