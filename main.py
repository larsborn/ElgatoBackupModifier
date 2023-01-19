#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import io
import json
import zipfile
from dataclasses import dataclass
from typing import Iterator


@dataclass
class ZipEntry:
    file_name: str
    compressed_size: int
    data: bytes
    timestamp: datetime.datetime


class InMemoryZip:
    def __init__(self, data: bytes):
        self.entries = list(self._list(zipfile.ZipFile(io.BytesIO(data))))

    @staticmethod
    def _list(z: zipfile.ZipFile) -> Iterator[ZipEntry]:
        for entry in z.infolist():
            with z.open(entry) as sub_file:
                yield ZipEntry(
                    file_name=entry.filename,
                    compressed_size=entry.compress_size,
                    data=sub_file.read(),
                    timestamp=datetime.datetime(
                        year=entry.date_time[0],
                        month=entry.date_time[1],
                        day=entry.date_time[2],
                        hour=entry.date_time[3],
                        minute=entry.date_time[4],
                        second=entry.date_time[5],
                    )
                )

    def pack(self) -> bytes:
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'a', compression=zipfile.ZIP_DEFLATED) as zp:
            for entry in self.entries:
                zp.writestr(entry.file_name, entry.data)

        return out.getvalue()


def main(file_name: str, print_output_type: bool, out_file_name: str, output_type: Optional[str]):
    with open(file_name, 'rb') as fp:
        z = InMemoryZip(fp.read())
    for entry in z.entries:
        if not entry.file_name.endswith('.json'):
            continue
        data = json.loads(entry.data.decode('utf-8'))
        if 'Controllers' not in data.keys():
            continue
        new_controllers = []
        for controller in data['Controllers']:
            actions = controller['Actions']
            new_actions = {}
            for tile_pos, action in actions.items():
                if 'Settings' in action \
                        and action['Settings'] is not None \
                        and 'outputType' in action['Settings'].keys():
                    if print_output_type:
                        print(f'{action["Settings"]["outputType"]} ({action["Settings"]["path"]})')
                    if output_type is not None:
                        action['Settings']['outputType'] = output_type
                new_actions[tile_pos] = action
            controller['Actions'] = new_actions
            new_controllers.append(controller)
        data['Controllers'] = new_controllers
        entry.data = json.dumps(data).encode('utf-8')

    with open(out_file_name, 'wb') as fp:
        fp.write(z.pack())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    parser.add_argument('out_file_name')
    parser.add_argument('--print-output-type', action='store_true')
    parser.add_argument('--set-output-type', default=None)
    args = parser.parse_args()

    main(
        args.file_name,
        args.print_output_type,
        args.out_file_name,
        args.set_output_type,
    )
