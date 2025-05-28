# Hướng dẫn giải quyết lỗi "non-fast-forward" trong Git

Lỗi "non-fast-forward" xảy ra khi nhánh local của bạn bị tụt lại so với nhánh remote. Để giải quyết lỗi này, bạn cần thực hiện các bước sau:

## Bước 1: Fetch các thay đổi mới nhất từ repository remote
Chạy lệnh sau để fetch các thay đổi mới nhất từ repository remote:
```sh
git fetch origin
```

## Bước 2: Merge các thay đổi vào nhánh local của bạn
Chạy lệnh sau để merge các thay đổi từ nhánh remote vào nhánh local của bạn:
```sh
git merge origin/<branch-name>
```
Thay thế `<branch-name>` bằng tên của nhánh của bạn.

## Bước 3: Giải quyết xung đột merge (nếu có)
Nếu có xung đột merge, bạn cần giải quyết chúng bằng cách chỉnh sửa các file bị xung đột và sau đó commit các thay đổi.

## Bước 4: Đẩy các thay đổi của bạn lên repository remote
Chạy lệnh sau để đẩy các thay đổi của bạn lên repository remote:
```sh
git push origin <branch-name>
```
Thay thế `<branch-name>` bằng tên của nhánh của bạn.

Sau khi hoàn thành các bước trên, lỗi "non-fast-forward" sẽ được giải quyết và bạn có thể tiếp tục làm việc với repository của mình.
