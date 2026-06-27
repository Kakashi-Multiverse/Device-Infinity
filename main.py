#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trình xử lý cấu hình hệ thống Galaxy A57 5G (SM-A576E)
Công cụ này hỗ trợ đọc, chỉnh sửa trực quan và xuất file #DEVICE_CONFIG.
"""

import os
from datetime import datetime

class DeviceConfigProcessor:
    def __init__(self, filepath=None):
        self.headers = []
        self.config_data = {}
        self.features = []
        
        if filepath:
            self.load_from_file(filepath)

    def load_from_file(self, filepath):
        """Đọc và phân tích cú pháp tệp cấu hình DEVICE_CONFIG"""
        if not os.path.exists(filepath):
            print(f"[-] Lỗi: Không tìm thấy tệp tin {filepath}")
            return False
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            self.headers = []
            self.config_data = {}
            self.features = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Lưu trữ các dòng tiêu đề comment của file
                if line.startswith("#"):
                    self.headers.append(line)
                    continue
                
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    
                    if key == "Features":
                        # Tách danh sách các tính năng (Features)
                        self.features = [f.strip() for f in val.split(",") if f.strip()]
                    else:
                        self.config_data[key] = val
            print(f"[+] Đã tải thành công cấu hình từ {filepath}")
            return True
        except Exception as e:
            print(f"[-] Lỗi khi đọc file: {e}")
            return False

    def get_property(self, key, default=None):
        """Lấy giá trị của một thuộc tính cấu hình"""
        return self.config_data.get(key, default)

    def set_property(self, key, value):
        """Cập nhật hoặc thêm mới thuộc tính cấu hình"""
        self.config_data[key] = str(value)

    def toggle_feature(self, feature_name, enable=True):
        """Bật hoặc tắt một tính năng trong danh sách Features"""
        if enable:
            if feature_name not in self.features:
                self.features.append(feature_name)
                print(f"[+] Đã thêm tính năng: {feature_name}")
        else:
            if feature_name in self.features:
                self.features.remove(feature_name)
                print(f"[-] Đã gỡ tính năng: {feature_name}")

    def save_to_file(self, filepath):
        """Xuất dữ liệu hiện tại ra tệp cấu hình chuẩn định dạng"""
        try:
            # Tạo hoặc cập nhật dòng thời gian chạy thực tế
            now_str = datetime.now().strftime("%a %b %d %H:%M:%S GMT+07:00 %Y")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Ghi tiêu đề bắt buộc
                f.write("#DEVICE_CONFIG\n")
                f.write(f"#{now_str}\n")
                
                # Ghi các thuộc tính cơ bản trước
                for key, val in sorted(self.config_data.items()):
                    if key not in ["Features", "Build.RADIO"]:
                        f.write(f"{key}={val}\n")
                
                # Ghi danh sách Features đã xử lý
                if self.features:
                    features_str = ",".join(self.features)
                    f.write(f"Features={features_str}\n")
                
                # Ghi các thuộc tính đặc thù cuối file
                if "Build.RADIO" in self.config_data:
                    f.write(f"Build.RADIO={self.config_data['Build.RADIO']}\n")
                    
            print(f"[+] Xuất tệp tin cấu hình thành công: {filepath}")
            return True
        except Exception as e:
            print(f"[-] Lỗi khi ghi tệp tin: {e}")
            return False


# --- Khởi chạy thử nghiệm chương trình ---
if __name__ == "__main__":
    print("=== Trình Khởi Tạo & Tối Ưu Cấu Hình Hệ Thống Galaxy A57 ===")
    
    # 1. Khởi tạo một đối tượng xử lý mới
    processor = DeviceConfigProcessor()
    
    # 2. Thiết lập các thông số phần cứng mặc định cho SM-A576E (Tháng 6/2026)
    processor.set_property("HasHardKeyboard", "false")
    processor.set_property("Build.HARDWARE", "s5e8865")
    processor.set_property("Build.BRAND", "samsung")
    processor.set_property("Build.VERSION.SDK_INT", "37")
    processor.set_property("Build.MODEL", "SM-A576E")
    processor.set_property("Build.DEVICE", "a57x")
    processor.set_property("Build.VERSION.RELEASE", "17")
    processor.set_property("Build.MANUFACTURER", "samsung")
    processor.set_property("UserReadableName", "samsung SM-A576E")
    processor.set_property("Build.RADIO", "A576EXXU1BZF2,A576EXXU1BZF2")
    processor.set_property("Client", "android-google,samsung,apple")
    
    # 3. Kích hoạt các cờ cấu hình Gaming cao cấp nhất
    processor.set_property("Support120FPS", "true")
    processor.set_property("SupportUltraHD", "true")
    processor.set_property("UnlockMaxGraphics", "true")
    processor.set_property("GraphicsEffects", "ultra")
    
    # 4. Thêm các chứng chỉ âm thanh, hình ảnh nâng cao vào danh sách Features
    processor.toggle_feature("android.hardware.sensor.proximity", True)
    processor.toggle_feature("android.hardware.audio.dolby.atmos", True)
    processor.toggle_feature("com.dolby.motion.dolby-vision", True)
    processor.toggle_feature("android.hardware.audio.dts", True)
    
    # 5. Tiến hành lưu tệp cấu hình mục tiêu
    output_filename = "device_config.txt"
    processor.save_to_file(output_filename)
    
    print("\n[Hoàn thành] Bạn có thể đẩy file 'device_config.txt' này trực tiếp lên GitHub của mình!")
