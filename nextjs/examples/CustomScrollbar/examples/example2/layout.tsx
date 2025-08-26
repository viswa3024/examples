import type { Metadata } from "next";
import "./globals.css";
import GlobalScrollbar from "@/components/GlobalScrollbar";

export const metadata: Metadata = {
  title: "My App",
  description: "With Global Custom Scrollbar",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <GlobalScrollbar>{children}</GlobalScrollbar>
      </body>
    </html>
  );
}
