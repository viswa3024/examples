// app/layout.tsx
import "./globals.css";
import GlobalCustomScrollbar from "@/components/GlobalCustomScrollbar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {/* mounts the auto-applier; it returns null but runs the script */}
        <GlobalCustomScrollbar />
        {children}
      </body>
    </html>
  );
}
