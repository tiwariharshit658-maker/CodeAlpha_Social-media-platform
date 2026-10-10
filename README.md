# Mini Social — Django

A beginner-friendly mini social media app with profiles, posts, comments, likes, and follows.
Uses Django authentication and SQLite by default.

## Windows / VS Code setup

1. Extract this ZIP and open the `mini_social_django` folder in VS Code.
2. In Terminal → New Terminal, run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. Open http://127.0.0.1:8000/
4. Admin panel: http://127.0.0.1:8000/admin/

If PowerShell blocks activation, run this once in that terminal:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
Then activate the environment again.

## Features
- Sign up, sign in, and sign out
- Profile page with bio and profile editing
- Create and delete your own posts
- Comment on posts
- Like / unlike posts
- Follow / unfollow users
- Feed with newest posts first
- SQLite database for users, profiles, posts, comments, likes, and follows

## Notes
This is a learning project, not a production deployment. Before deploying publicly, add production settings, secure secrets, HTTPS, rate limiting, and moderation/reporting tools.
