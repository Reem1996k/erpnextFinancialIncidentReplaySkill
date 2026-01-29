import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Financial Incident Replay - Enterprise Platform",
  description: "Financial discrepancy analysis platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header className="app-header">
          <div className="app-title">Financial Incident Replay</div>
          <nav className="app-nav">
            <a href="/">Create Incident</a>
            <a href="/incidents">Incidents</a>
          </nav>
        </header>

        <main className="main-content">
          {children}
        </main>

        <style>{`
          .app-header {
            height: 64px;
            background-color: #1e3a8a;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 50;
          }

          .app-title {
            color: white;
            font-size: 18px;
            font-weight: 600;
          }

          .app-nav {
            display: flex;
            gap: 32px;
          }

          .app-nav a {
            color: #e0e7ff;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
          }

          .app-nav a:hover {
            color: white;
            text-decoration: underline;
          }

          .main-content {
            padding-top: 64px;
          }

          body {
            margin: 0;
            padding: 0;
            background-color: #f1f7ff;
          }
        `}</style>
      </body>
    </html>
  );
}
