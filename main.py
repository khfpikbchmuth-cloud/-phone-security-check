
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import platform
import socket
import subprocess
import shutil
import os


def command(args):
    if not shutil.which(args[0]):
        return "در دسترس نیست"
    try:
        r = subprocess.run(
            args, capture_output=True,
            text=True, timeout=5
        )
        return (r.stdout or r.stderr).strip() or "اطلاعاتی یافت نشد"
    except Exception:
        return "خطا در اجرا"


def getprop(name):
    return command(["getprop", name])


def device_info():
    print("\n=== اطلاعات دستگاه ===")

    items = {
        "سازنده": getprop("ro.product.manufacturer"),
        "مدل": getprop("ro.product.model"),
        "اندروید": getprop("ro.build.version.release"),
        "پردازنده": getprop("ro.product.cpu.abi"),
        "پایتون": platform.python_version()
    }

    for key, value in items.items():
        print(f"{key}: {value}")

    return items


def network_check():
    print("\n=== بررسی شبکه ===")
    results = {}

    try:
        ip = socket.gethostbyname("example.com")
        print("DNS: موفق")
        results["DNS"] = f"موفق: {ip}"
    except Exception:
        print("DNS: ناموفق")
        results["DNS"] = "ناموفق"

    try:
        socket.create_connection(
            ("1.1.1.1", 443), timeout=4
        ).close()
        print("اتصال اینترنت: موفق")
        results["Internet"] = "موفق"
    except Exception:
        print("اتصال اینترنت: ناموفق")
        results["Internet"] = "ناموفق"

    dns = getprop("net.dns1")
    print("DNS سیستم:", dns)
    results["DNS سیستم"] = dns

    return results


def security_check():
    print("\n=== بررسی تنظیمات امنیتی ===")

    items = {
        "Debuggable": getprop("ro.debuggable"),
        "Secure": getprop("ro.secure"),
        "Verified Boot": getprop(
            "ro.boot.verifiedbootstate"
        )
    }

    for key, value in items.items():
        print(f"{key}: {value}")

    return items


def full_scan():
    print("\nشروع بررسی کامل تلفن...")

    sections = [
        ("اطلاعات دستگاه", device_info),
        ("شبکه", network_check),
        ("امنیت", security_check)
    ]

    report = [
        "گزارش بررسی امنیت تلفن",
        datetime.datetime.now().astimezone().isoformat()
    ]

    for title, function in sections:
        report.append("\n" + title)
        for key, value in function().items():
            report.append(f"{key}: {value}")

    filename = "security_report.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("\nگزارش ذخیره شد:", os.path.abspath(filename))


def main():
    while True:
        print("""
==============================
     بررسی امنیت تلفن
==============================
1. بررسی کامل گوشی
2. اطلاعات دستگاه
3. بررسی شبکه و DNS
4. بررسی تنظیمات امنیتی
5. خروج
""")

        choice = input("انتخاب کنید: ").strip()

        if choice == "1":
            full_scan()
        elif choice == "2":
            device_info()
        elif choice == "3":
            network_check()
        elif choice == "4":
            security_check()
        elif choice == "5":
            print("خروج از برنامه")
            break
        else:
            print("گزینه نامعتبر است")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nبرنامه متوقف شد")
