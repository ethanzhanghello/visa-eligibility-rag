import './globals.css'
import type { Metadata } from 'next'
import { Inter, Noto_Sans_SC } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })
const notoSansSC = Noto_Sans_SC({ subsets: ['latin'], weight: ['400', '500', '600', '700'] })

export const metadata: Metadata = {
  title: 'Green Card RAG Helper',
  description: 'A bilingual web application to help users determine their eligibility for U.S. green card categories',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.className} ${notoSansSC.className}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
} 