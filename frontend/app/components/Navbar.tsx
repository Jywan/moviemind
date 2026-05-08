"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
    { href: "/", label: "대시보드" },
    { href: "/analysis", label: "분석" },
    { href: "/recommend", label: "추천" },
];


export default function Navbar() {
    const pathname = usePathname();

    return (
        <nav className="bg-white shadow-sm px-8 py-4 flex items-center gap-8">
            <span className="text-xl font-bold text-indigo-600">MovieMind</span>
            <div className="flex gap-6">
                {navItems.map((item) => (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={`text-sm font-medium ${
                            pathname === item.href 
                                ? "text-indigo-600 border-b-2 border-indigo-600 pb-1"
                                : "text-gray-500 hover:text-gray-800"
                        }`}
                    >
                        {item.label}
                    </Link>
                ))}
            </div>
        </nav>
    );
}