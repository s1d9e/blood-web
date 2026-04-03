#!/usr/bin/env python3
"""
Blood-Web Monitoring Dashboard
Real-time web interface for honeypot monitoring.
"""

import http.server
import socketserver
import json
import os
import threading
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

DARK_THEME = """
<!DOCTYPE html>
<html>
<head>
    <title>Blood-Web Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 50%, #0a0a0a 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: rgba(139, 0, 0, 0.3);
            border: 2px solid #8b0000;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 0 30px rgba(139, 0, 0, 0.5);
        }
        .header h1 {
            font-size: 2.5em;
            color: #ff4444;
            text-shadow: 0 0 10px #ff0000, 0 0 20px #8b0000;
            margin-bottom: 10px;
        }
        .header p {
            color: #ff8888;
            font-style: italic;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            border-color: #8b0000;
            box-shadow: 0 0 15px rgba(139, 0, 0, 0.3);
            transform: translateY(-5px);
        }
        .stat-card .value {
            font-size: 2.5em;
            font-weight: bold;
            color: #ff4444;
        }
        .stat-card .label {
            color: #888;
            text-transform: uppercase;
            font-size: 0.8em;
            letter-spacing: 2px;
        }
        .stat-card.critical .value { color: #ff0000; }
        .stat-card.high .value { color: #ff6600; }
        .stat-card.medium .value { color: #ffcc00; }
        .stat-card.low .value { color: #00ff00; }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        @media (max-width: 1000px) {
            .container { grid-template-columns: 1fr; }
        }
        .panel {
            background: rgba(20, 20, 20, 0.95);
            border: 1px solid #333;
            border-radius: 8px;
            overflow: hidden;
        }
        .panel-header {
            background: linear-gradient(90deg, #8b0000, #4a0000);
            padding: 15px 20px;
            font-size: 1.2em;
            color: #fff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .panel-header .count {
            background: rgba(0,0,0,0.3);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
        }
        .panel-content {
            padding: 0;
            max-height: 400px;
            overflow-y: auto;
        }
        .panel-content::-webkit-scrollbar {
            width: 8px;
        }
        .panel-content::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        .panel-content::-webkit-scrollbar-thumb {
            background: #8b0000;
            border-radius: 4px;
        }
        .attack-item {
            padding: 12px 20px;
            border-bottom: 1px solid #222;
            display: grid;
            grid-template-columns: 150px 1fr 100px;
            gap: 15px;
            align-items: center;
            transition: background 0.2s;
        }
        .attack-item:hover {
            background: rgba(139, 0, 0, 0.1);
        }
        .attack-item .time {
            color: #666;
            font-size: 0.85em;
        }
        .attack-item .source {
            color: #ff6666;
            font-weight: bold;
        }
        .attack-item .technique {
            font-size: 0.9em;
        }
        .severity-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 0.75em;
            text-transform: uppercase;
            font-weight: bold;
        }
        .severity-critical { background: #8b0000; color: #fff; }
        .severity-high { background: #ff3300; color: #fff; }
        .severity-medium { background: #cc9900; color: #000; }
        .severity-low { background: #006600; color: #fff; }
        .chart-container {
            padding: 20px;
            height: 200px;
        }
        .service-list {
            padding: 10px 20px;
        }
        .service-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #222;
        }
        .service-item:last-child { border-bottom: none; }
        .service-name {
            color: #ff8888;
            font-weight: bold;
        }
        .service-port {
            color: #666;
        }
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active { background: #00ff00; box-shadow: 0 0 5px #00ff00; }
        .status-inactive { background: #ff0000; }
        .live-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #00ff00;
        }
        .live-dot {
            width: 8px;
            height: 8px;
            background: #00ff00;
            border-radius: 50%;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
        .top-ips {
            padding: 10px 20px;
        }
        .ip-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #222;
        }
        .ip-item .count {
            color: #ff4444;
            font-weight: bold;
        }
        .refresh-btn {
            background: #8b0000;
            border: none;
            color: white;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.3s;
        }
        .refresh-btn:hover {
            background: #aa0000;
            box-shadow: 0 0 10px rgba(139, 0, 0, 0.5);
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Blood-Web Monitor</h1>
        <p>"All that and a bag of chips..."</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="value" id="total-attacks">0</div>
            <div class="label">Total Attacks</div>
        </div>
        <div class="stat-card critical">
            <div class="value" id="critical-count">0</div>
            <div class="label">Critical</div>
        </div>
        <div class="stat-card high">
            <div class="value" id="high-count">0</div>
            <div class="label">High</div>
        </div>
        <div class="stat-card medium">
            <div class="value" id="medium-count">0</div>
            <div class="label">Medium</div>
        </div>
        <div class="stat-card low">
            <div class="value" id="low-count">0</div>
            <div class="label">Low</div>
        </div>
    </div>
    
    <div class="container">
        <div class="panel">
            <div class="panel-header">
                <span><span class="live-indicator"><span class="live-dot"></span>LIVE FEED</span></span>
                <span class="count" id="feed-count">0</span>
            </div>
            <div class="panel-content" id="attack-feed">
                <div style="padding: 20px; color: #666; text-align: center;">
                    Waiting for attacks...
                </div>
            </div>
        </div>
        
        <div>
            <div class="panel" style="margin-bottom: 20px;">
                <div class="panel-header">
                    <span>Top Attackers</span>
                </div>
                <div class="top-ips" id="top-ips">
                    <div style="color: #666; text-align: center; padding: 20px;">
                        No data yet
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">
                    <span>Attacks by Service</span>
                </div>
                <div class="service-list" id="service-stats">
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>SSH</span>
                        <span class="service-port">Port 2222</span>
                        <span id="ssh-count">0</span>
                    </div>
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>FTP</span>
                        <span class="service-port">Port 2121</span>
                        <span id="ftp-count">0</span>
                    </div>
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>HTTP</span>
                        <span class="service-port">Port 8080</span>
                        <span id="http-count">0</span>
                    </div>
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>Telnet</span>
                        <span class="service-port">Port 2323</span>
                        <span id="telnet-count">0</span>
                    </div>
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>SMB</span>
                        <span class="service-port">Port 4445</span>
                        <span id="smb-count">0</span>
                    </div>
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>MySQL</span>
                        <span class="service-port">Port 3306</span>
                        <span id="mysql-count">0</span>
                    </div>
                    <div class="service-item">
                        <span><span class="status-dot status-active"></span>RDP</span>
                        <span class="service-port">Port 3389</span>
                        <span id="rdp-count">0</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Blood-Web Honeypot v1.0 | <button class="refresh-btn" onclick="location.reload()">Refresh</button></p>
    </div>
    
    <script>
        let attackData = [];
        let updateInterval;
        
        async function fetchData() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                updateDashboard(data);
            } catch (e) {
                console.log('Waiting for data...');
            }
        }
        
        function updateDashboard(data) {
            if (!data || !data.attacks) return;
            
            document.getElementById('total-attacks').textContent = data.total || 0;
            document.getElementById('critical-count').textContent = data.severity?.CRITICAL || 0;
            document.getElementById('high-count').textContent = data.severity?.HIGH || 0;
            document.getElementById('medium-count').textContent = data.severity?.MEDIUM || 0;
            document.getElementById('low-count').textContent = data.severity?.LOW || 0;
            
            const services = data.by_service || {};
            document.getElementById('ssh-count').textContent = services.ssh || 0;
            document.getElementById('ftp-count').textContent = services.ftp || 0;
            document.getElementById('http-count').textContent = services.http || 0;
            document.getElementById('telnet-count').textContent = services.telnet || 0;
            document.getElementById('smb-count').textContent = services.smb || 0;
            document.getElementById('mysql-count').textContent = services.mysql || 0;
            document.getElementById('rdp-count').textContent = services.rdp || 0;
            
            const topIps = data.top_ips || [];
            const ipsContainer = document.getElementById('top-ips');
            if (topIps.length > 0) {
                ipsContainer.innerHTML = topIps.map(ip => 
                    '<div class="ip-item"><span class="source">' + ip.ip + '</span><span class="count">' + ip.count + '</span></div>'
                ).join('');
            }
            
            const attacks = data.attacks.slice(-20).reverse();
            const feedContainer = document.getElementById('attack-feed');
            document.getElementById('feed-count').textContent = data.attacks.length;
            
            if (attacks.length > 0) {
                feedContainer.innerHTML = attacks.map(atk => {
                    const time = new Date(atk.timestamp).toLocaleTimeString();
                    const severity = atk.severity.toLowerCase();
                    return '<div class="attack-item">' +
                        '<span class="time">' + time + '</span>' +
                        '<span class="source">' + atk.source_ip + '</span>' +
                        '<span class="technique"><span class="severity-badge severity-' + severity + '">' + atk.technique + '</span></span>' +
                        '</div>';
                }).join('');
            }
            
            attackData = data;
        }
        
        fetchData();
        setInterval(fetchData, 3000);
    </script>
</body>
</html>
"""


class AttackTracker:
    """Tracks attacks from log files"""
    
    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = log_dir
        self.attacks: List[Dict] = []
        self._parse_logs()
        
    def _parse_logs(self):
        """Parse existing log files"""
        if not os.path.exists(self.log_dir):
            return
            
        for filename in sorted(os.listdir(self.log_dir)):
            if filename.startswith('attacks_') and filename.endswith('.log'):
                filepath = os.path.join(self.log_dir, filename)
                self._parse_log_file(filepath)
                
    def _parse_log_file(self, filepath: str):
        """Parse a single log file"""
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split(' | ')
                    if len(parts) >= 4:
                        timestamp = parts[0]
                        source = parts[1].split(' -> ')
                        service = source[1] if len(source) > 1 else 'unknown'
                        source_ip = source[0].split(':')[0] if source else 'unknown'
                        technique = parts[2]
                        severity = parts[3].replace('Severity: ', '')
                        
                        self.attacks.append({
                            'timestamp': timestamp,
                            'source_ip': source_ip,
                            'service': service.lower(),
                            'technique': technique,
                            'severity': severity
                        })
        except Exception as e:
            pass
            
    def get_stats(self) -> Dict:
        """Get attack statistics"""
        severity_counts = defaultdict(int)
        service_counts = defaultdict(int)
        ip_counts = defaultdict(int)
        
        for attack in self.attacks:
            severity_counts[attack['severity']] += 1
            service_counts[attack['service']] += 1
            ip_counts[attack['source_ip']] += 1
            
        top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total': len(self.attacks),
            'severity': dict(severity_counts),
            'by_service': dict(service_counts),
            'top_ips': [{'ip': ip, 'count': count} for ip, count in top_ips],
            'attacks': self.attacks[-100:]
        }
        
    def refresh(self):
        """Refresh data from log files"""
        self.attacks = []
        self._parse_logs()


class MonitorHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for monitoring dashboard"""
    
    tracker: AttackTracker = None
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(DARK_THEME.encode())
            
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats = self.tracker.get_stats()
            self.wfile.write(json.dumps(stats, indent=2).encode())
            
        elif self.path == '/api/refresh':
            self.tracker.refresh()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        else:
            super().do_GET()
            
    def log_message(self, format, *args):
        pass


class MonitoringServer:
    """Monitoring web server"""
    
    def __init__(self, port: int = 8081, log_dir: str = 'logs'):
        self.port = port
        self.log_dir = log_dir
        self.tracker = AttackTracker(log_dir)
        self.server = None
        
    def start(self):
        """Start the monitoring server"""
        MonitorHandler.tracker = self.tracker
        
        self.server = socketserver.TCPServer(('', self.port), MonitorHandler)
        self.server.allow_reuse_address = True
        
        print(f"""
╔══════════════════════════════════════════════════════════╗
║           Blood-Web Monitoring Dashboard                  ║
╚══════════════════════════════════════════════════════════╝
  [+] Dashboard URL: http://localhost:{self.port}
  [+] API Endpoint:  http://localhost:{self.port}/api/stats
  [+] Refresh:       http://localhost:{self.port}/api/refresh
  
  Press Ctrl+C to stop the dashboard
""")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Shutting down dashboard...")
            self.server.shutdown()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Blood-Web Monitoring Dashboard')
    parser.add_argument('--port', type=int, default=8081, help='Dashboard port (default: 8081)')
    parser.add_argument('--log-dir', default='logs', help='Log directory')
    
    args = parser.parse_args()
    
    server = MonitoringServer(port=args.port, log_dir=args.log_dir)
    server.start()


if __name__ == '__main__':
    main()
