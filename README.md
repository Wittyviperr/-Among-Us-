# -Among-Us-

Among Us - Multiplayer Game Dashboard
Overview
This project is a web-based Among Us-inspired Multiplayer Game Dashboard where players and an admin interact through a visually appealing and user-friendly interface. The platform is designed to replicate core functionalities of the game, such as assigning tasks, tracking alive and dead players, and handling emergency meetings and voting. It incorporates a dynamic admin panel for complete control over the game.

Features
Player Dashboard
Dynamic Role Assignment: Players log in to their dashboards and are assigned roles (Crewmate or Imposter).

Task Management: Each Crewmate is assigned a unique set of tasks by the admin.

Game Status Tracking: Displays the remaining time, alive and dead players, and whether the game is paused.

Emergency Meetings: Players can call an emergency meeting during the game to pause the timer and initiate discussions.

Interactive Broadcasts: Admin messages (e.g., "Imposter Ejected!" or "Crewmates Win!") are shown as pop-ups in a stylish modal.

Logout Functionality: Secure logout option to exit the game.

Admin Dashboard
Game Control:

Start, pause, resume, or restart the game.

Initiate and stop voting during emergency meetings.

Task Assignment: Admin can assign tasks to any alive player.

Player Management:

Mark players as dead.

Broadcast custom messages (e.g., "Imposter Wins!" or "Crewmates Win!") to all players.

Live Player Details: Displays player statuses (alive/dead), roles, and assigned tasks in real-time.

Design
Theme: Inspired by the "Among Us" game, featuring a dark, space-themed background with vibrant neon highlights.

Responsive UI: Optimized for desktop and mobile users.

Interactive Elements:

Bootstrap-powered modals for broadcast messages.

Dynamic updates for game stats using JavaScript and Flask.

Tech Stack
Frontend:

HTML5, CSS3

JavaScript (Bootstrap Framework for UI)

Backend:

Flask (Python-based web framework)

Jinja2 (Template engine for dynamic content)

Deployment:

Compatible with platforms like Heroku, AWS, or any Flask-compatible environment.
