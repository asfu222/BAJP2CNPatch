import struct
from io import BytesIO
from typing import Any, Dict, List
import binascii
import os

def from_bytes(bytes_data: bytes) -> Dict[str, Any]:
    cursor = BytesIO(initial_bytes=bytes_data)

    def read_i8() -> Any:
        return struct.unpack('b', cursor.read(1))[0]

    def read_i32() -> Any:
        return struct.unpack('i', cursor.read(4))[0]

    def read_i64() -> Any:
        return struct.unpack('q', cursor.read(8))[0]

    def read_bool() -> Any:
        return struct.unpack('?', cursor.read(1))[0]

    def read_string() -> str:
        length = read_i32()
        return cursor.read(length).decode('utf-8', errors='replace')

    def read_includes() -> List[str]:
        size = read_i32()
        if size == -1:
            return []
        _ = read_i32()  # Skip 4 bytes
        includes: list = []

        for _ in range(size):
            includes.append(read_string())
            if _ != size - 1:
                _ = read_i32()  # Skip 4 bytes
        return includes

    def read_table() -> tuple[str, dict[str, Any]]:
        _ = read_i32()  # Skip 4 bytes
        key: str = read_string()
        _ = read_i8()  # Skip 1 byte
        _ = read_i32()  # Skip 4 bytes
        name: str = read_string()
        size = read_i64()
        crc = read_i64()
        is_in_build = read_bool()
        is_changed = read_bool()
        is_prologue = read_bool()
        is_split_download = read_bool()
        includes: List[str] = read_includes()

        return key, {
            'name': name,
            'size': size,
            'crc': crc,
            'is_in_build': is_in_build,
            'is_changed': is_changed,
            'is_prologue': is_prologue,
            'is_split_download': is_split_download,
            'includes': includes,
        }

    _ = read_i8()  # Skip 1 byte
    data_size = read_i32()
    data: dict = {}

    for _ in range(data_size):
        key, value = read_table()
        data[key] = value

    return data

def from_json(data: Dict[str, Any]) -> bytes:
    def write_i8(value: int, buffer: bytearray) -> None:
        buffer.extend(struct.pack('b', value))

    def write_i32(value: int, buffer: bytearray) -> None:
        buffer.extend(struct.pack('i', value))

    def write_i64(value: int, buffer: bytearray) -> None:
        buffer.extend(struct.pack('q', value))

    def write_bool(value: bool, buffer: bytearray) -> None:
        buffer.extend(struct.pack('?', value))

    def write_string(value: str, buffer: bytearray) -> None:
        encoded = value.encode('utf-8')
        write_i32(len(encoded), buffer)
        buffer.extend(encoded)

    def write_includes(includes: list[str], buffer: bytearray) -> None:
        if not includes:
            write_i32(-1, buffer)  # No includes
            return

        write_i32(len(includes), buffer)
        write_i32(0, buffer)  # Placeholder for skipped 4 bytes

        for include in includes:
            write_string(include, buffer)
            if include != includes[-1]:
                write_i32(0, buffer)  # Placeholder for skipped 4 bytes

    def write_table(key: str, value: dict, buffer: bytearray) -> None:
        write_i32(0, buffer)  # Placeholder for skipped 4 bytes
        write_string(key, buffer)
        write_i8(0, buffer)  # Placeholder for skipped 1 byte
        write_i32(0, buffer)  # Placeholder for skipped 4 bytes
        write_string(value['name'], buffer)
        write_i64(value['size'], buffer)
        write_i64(value['crc'], buffer)
        write_bool(value['is_in_build'], buffer)
        write_bool(value['is_changed'], buffer)
        write_bool(value['is_prologue'], buffer)
        write_bool(value['is_split_download'], buffer)
        write_includes(value['includes'], buffer)

    buffer = bytearray()

    write_i8(0, buffer)  # Placeholder for skipped 1 byte
    write_i32(len(data), buffer)

    for key, value in data.items():
        write_table(key, value, buffer)

    return bytes(buffer)
def calculate_crc32(file_path) -> int:
    with open(file_path, 'rb') as f:
        return binascii.crc32(f.read()) & 0xFFFFFFFF
json_data = None
with open('./TableCatalog.bytes', 'rb') as f:
    json_data = from_bytes(f.read())

size = os.path.getsize('./ExcelDB.db')
crc = calculate_crc32('./ExcelDB.db')
print(f"TableCatalog.bytes: 修改ExcelDB.db 文件大小值 {json_data['ExcelDB.db']['size']} -> {size}")
print(f"TableCatalog.bytes: 修改ExcelDB.db crc值 {json_data['ExcelDB.db']['crc']} -> {crc}")
json_data['ExcelDB.db']['size'] = size
json_data['ExcelDB.db']['crc'] = crc
patched_bytes_data = from_json(json_data)

with open('./TableCatalog.bytes', 'wb') as f:
    f.write(patched_bytes_data)
print('已生成对应ExcelDB.db的TableCatalog.bytes')