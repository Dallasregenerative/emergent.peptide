module.exports = {
  apps: [
    {
      name: 'peptide-backend',
      script: 'backend/server.py',
      interpreter: 'python3',
      cwd: '/var/www/peptideprotocols',
      env: {
        NODE_ENV: 'production',
        PORT: 8001
      },
      error_file: '/var/log/peptide-backend-error.log',
      out_file: '/var/log/peptide-backend-out.log',
      log_file: '/var/log/peptide-backend.log',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    },
    {
      name: 'peptide-frontend',
      script: 'serve',
      args: '-s frontend/build -l 3000',
      cwd: '/var/www/peptideprotocols',
      env: {
        NODE_ENV: 'production'
      },
      error_file: '/var/log/peptide-frontend-error.log',
      out_file: '/var/log/peptide-frontend-out.log',
      log_file: '/var/log/peptide-frontend.log',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M'
    }
  ]
};