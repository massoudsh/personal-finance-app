import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Personal Finance App',
  description: 'Manage your personal finances',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

