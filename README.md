# Giải thích thuật toán hiệu chỉnh Camera–LiDAR

Tài liệu này giải thích **bằng tiếng Việt, dễ hiểu** các ý sau:

- Vì sao phải hiệu chỉnh ngoại (extrinsic calibration) giữa camera và LiDAR.
- Mô hình toán học: *rigid transform* (quay + tịnh tiến) giữa hai hệ trục.
- Thuật toán **Kabsch / Umeyama** dùng trong file
  `my_robot/perception/cam_lidar_calib_example.py`.
- Cách lấy kết quả (R, t) và đưa vào URDF (`walle_cam_lidar_calib_example.urdf.xacro`).

---

## 1. Bản chất bài toán: gộp hai hệ trục về một

Robot có 2 cảm biến chính:

- **Camera RGB‑D D435i** – xuất ra toạ độ 3D trong hệ *camera* (frame `camera_link`).
- **LiDAR** – xuất ra toạ độ 2D/3D trong hệ *LiDAR* (frame `lidar_link`).

Mỗi cảm biến có **gốc (0,0,0)** và **ba trục X,Y,Z riêng**. Vì vậy cùng một vật A ngoài đời:

- Camera có thể nói: "A ở $(1.8, 0.0, 0.1)$ m".
- LiDAR có thể nói: "A ở $(2.0, 0.0, 0.0)$ m".

Hai con số này **không so sánh trực tiếp được** vì đo trong **hai hệ trục khác nhau**.

Mục tiêu của hiệu chỉnh ngoại là tìm một phép biến đổi cố định để
luôn có thể đổi điểm từ hệ LiDAR sang hệ camera (hoặc ngược lại). Ta mô hình hoá bằng:

$$
 p_C = R_{CL} \, p_L + t_{CL}
$$

trong đó:

- $p_L = [x_L, y_L, z_L]^T$ – toạ độ điểm trong hệ LiDAR (`lidar_link`).
- $p_C = [x_C, y_C, z_C]^T$ – toạ độ **cùng điểm đó** nhưng trong hệ camera (`camera_link`).
- $R_{CL}$ – ma trận quay $3\times3$, biến đổi hướng trục LiDAR cho trùng với trục camera.
- $t_{CL} = [t_x, t_y, t_z]^T$ – vector tịnh tiến: vị trí gốc LiDAR so với gốc camera.

Đây là **phép biến đổi cứng 3D (rigid transform)** – chỉ gồm quay + tịnh tiến, không kéo giãn.

Khoảng cách giữa hai "tâm" cảm biến chính là độ dài của $t_{CL}$:

$$
 d = \|t_{CL}\|_2 = \sqrt{t_x^2 + t_y^2 + t_z^2}.
$$

Sau khi đã biết $R_{CL}, t_{CL}$, ta có thể:

- Đổi mọi điểm LiDAR về hệ camera → so sánh trực tiếp với depth.
- Đưa cả hai về một frame khác (ví dụ `base_link`, `map`) thông qua TF chain của ROS.

---

## 2. Lấy dữ liệu để giải bài toán

Ta cần **các cặp điểm tương ứng** mà cả hai cảm biến đều đo được.

### 2.1. Chọn mốc chung (marker)

- Dán **ArUco marker** hoặc một tấm vuông dễ nhận ra lên mặt phẳng.
- Đặt marker tại nhiều vị trí khác nhau quanh robot, sao cho:
  - Camera thấy được marker → trích toạ độ 3D bằng depth.
  - LiDAR quét trúng marker → trích toạ độ điểm/cụm điểm tương ứng.

### 2.2. Tạo hai mảng điểm tương ứng

Ta cần nhiều cặp điểm $\bigl(p_L^{(i)}, p_C^{(i)}\bigr)$ sao cho **đó là cùng một mốc ngoài đời**.

Với mỗi lần đặt marker thứ $i$:

1. **Từ camera (frame `camera_link`)**

   - Phát hiện marker trong ảnh màu (OpenCV ArUco).
   - Lấy điểm tâm marker trên ảnh, đọc giá trị depth tương ứng, back‑project ra 3D:

     $$
     p_C^{(i)} = [x_C^{(i)}, y_C^{(i)}, z_C^{(i)}]^T.
     $$

   - Ý nghĩa: $x_C^{(i)}, y_C^{(i)}, z_C^{(i)}$ là toạ độ của mốc thứ $i$ trong hệ camera.

2. **Từ LiDAR (frame `lidar_link`)**

   - Dùng thuật toán đơn giản (cluster theo khoảng cách) để lấy cụm điểm tương ứng mặt marker.
   - Lấy trung bình cụm điểm đó → toạ độ mốc trong hệ LiDAR:

     $$
     p_L^{(i)} = [x_L^{(i)}, y_L^{(i)}, z_L^{(i)}]^T.
     $$

   - Với LiDAR 2D, toàn bộ điểm nằm trên mặt phẳng quét, ta có thể đặt
     $$z_L^{(i)} = 0.$$

Sau khi lặp lại $N$ lần (nhiều vị trí marker khác nhau quanh robot), ta có:

- Mảng `points_L` kích thước $(N, 3)$ chứa các $p_L^{(i)}$.
- Mảng `points_C` kích thước $(N, 3)$ chứa các $p_C^{(i)}$.

Mục tiêu: tìm $R_{CL}, t_{CL}$ sao cho cho mọi $i$:

$$
 p_C^{(i)} \approx R_{CL} \, p_L^{(i)} + t_{CL}.
$$

Nói cách khác: **tìm phép quay + tịnh tiến sao cho hai đám mây điểm (LiDAR và camera)
chồng khớp lên nhau tốt nhất**.

---

## 3. Thuật toán Kabsch / Umeyama (SVD rigid alignment)

Thuật toán trong file `cam_lidar_calib_example.py` là biến thể Kabsch/Umeyama, gồm 6 bước chính.

### Bước 1 – Tính tâm hai tập điểm

Tâm (mean) của hai tập:

$$
 \bar{p}_L = \frac{1}{N} \sum_{i=1}^N p_L^{(i)}, \qquad
 \bar{p}_C = \frac{1}{N} \sum_{i=1}^N p_C^{(i)}.
$$

### Bước 2 – Dịch điểm về gốc

Trừ tâm khỏi từng điểm, ta được các điểm mới nằm quanh gốc $(0,0,0)$:

$$
 	ilde{p}_L^{(i)} = p_L^{(i)} - \bar{p}_L, \qquad
 	ilde{p}_C^{(i)} = p_C^{(i)} - \bar{p}_C.
$$

Ý nghĩa trực giác: tạm thời **bỏ qua tịnh tiến**, chỉ quan tâm đến quay.

### Bước 3 – Ma trận hiệp phương sai

Tạo ma trận $H$:

$$
 H = \sum_{i=1}^N \tilde{p}_L^{(i)} (\tilde{p}_C^{(i)})^T.
$$

- $H$ là ma trận $3\times 3$ mô tả tương quan giữa hướng của hai bộ điểm.
- Nếu hai tập giống nhau, $H$ sẽ gần với ma trận quay thật nhân với ma trận đối xứng.

### Bước 4 – Phân rã SVD

Tính SVD:

$$
 H = U \, \Sigma \, V^T
$$

trong đó:

- $U$, $V$ là các ma trận trực chuẩn ($U U^T = V V^T = I$).
- $\Sigma$ là ma trận đường chéo chứa các giá trị riêng (singular values).

### Bước 5 – Ma trận quay tối ưu

Ma trận quay tối ưu (theo nghĩa **ít sai số bình phương nhất**) là:

$$
 R_{CL} = V U^T.
$$

Nếu $\det(R_{CL}) < 0$ (bị lật gương), ta sửa bằng cách đổi dấu cột cuối của $V$ rồi tính lại.

Trực giác:

- SVD tìm ra cách quay hệ LiDAR để trùng với hệ camera sao cho hai đám mây điểm **khớp nhau nhất**.

### Bước 6 – Vector tịnh tiến

Sau khi đã có quay, tịnh tiến được tính sao cho tâm hai tập trùng nhau:

$$
 t_{CL} = \bar{p}_C - R_{CL} \, \bar{p}_L.
$$

Khi đó với mọi $i$:

$$
 p_C^{(i)} \approx R_{CL} \, p_L^{(i)} + t_{CL}.
$$

### Sai số RMS (để biết hiệu chỉnh tốt hay kém)

Ta có thể tính sai số còn lại cho từng điểm:

$$
 e_i = p_C^{(i)} - (R_{CL} \, p_L^{(i)} + t_{CL})
$$

Trong đó $e_i$ là vectơ sai số giữa điểm đo từ camera và điểm LiDAR đã đổi sang hệ camera.

Sai số trung bình bình phương (RMSE):

$$
 	ext{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N \lVert e_i \rVert^2}.
$$

- RMSE càng nhỏ (vài mm–cm) → hiệu chỉnh càng tốt.
- Nếu RMSE lớn → cần thêm điểm, đo lại, hoặc setup marker rõ hơn.

Trong code, hàm `kabsch_align` trả về cả `transform` và `rmse`.

---

## 4. Liên hệ với file Python `cam_lidar_calib_example.py`

### 4.1. Lớp `RigidTransform`

Trong file có lớp:

- `RigidTransform(R, t)` lưu:
  - `R`: ma trận quay từ LiDAR sang camera.
  - `t`: vector tịnh tiến từ camera tới LiDAR.
- Thuộc tính `distance` = `np.linalg.norm(t)`: khoảng cách giữa hai tâm.
- Hàm `transform(p_L)` áp dụng công thức:

  ```python
  p_C = (R @ p_L.T).T + t
  ```

### 4.2. Hàm `kabsch_align(points_L, points_C)`

Cài đặt đúng 6 bước trên:

1. Kiểm tra kích thước mảng.
2. Tính `mean_L`, `mean_C`.
3. Tính `q_L`, `q_C` (đã trừ mean).
4. Tính `H = q_L.T @ q_C`.
5. SVD `U, S, Vt = np.linalg.svd(H)` rồi `R = Vt.T @ U.T`.
6. `t = mean_C - R @ mean_L`.
7. Tính RMSE từ chênh lệch giữa điểm dự đoán và điểm thật.

Kết quả:

```python
transform, rmse = kabsch_align(points_L, points_C)
print(transform.R)  # ma trận quay
print(transform.t)  # vector tịnh tiến (xyz trong hệ camera)
print(transform.distance)  # khoảng cách tâm–tâm
print(rmse)  # sai số RMS
```

### 4.3. Hàm `demo_synthetic()`

Demo này chỉ để bạn hiểu trực giác:

- Tạo "transform thật" `t_true = [-0.10, 0, 0.10]` (LiDAR sau 10cm, cao hơn 10cm).
- Sinh vài điểm trong hệ LiDAR, áp dụng transform thật để ra điểm trong hệ camera.
- Thêm nhiễu nhỏ (~5 mm).
- Gọi `kabsch_align` để xem thuật toán có tìm lại gần đúng t_true hay không.

Bạn có thể chạy:

```bash
cd My-Robot-main/my_robot
python -m my_robot.perception.cam_lidar_calib_example
```

và quan sát `t_true` vs `t_est`.

---

## 5. Đưa kết quả vào URDF

Sau khi hiệu chỉnh với dữ liệu thật (thay dữ liệu giả trong demo bằng `points_L`, `points_C` thật), bạn lấy:

- `t_est = transform.t = [t_x, t_y, t_z]` (đơn vị: mét, trong hệ camera_link).
- Nếu cần: tính roll/pitch/yaw từ `R_est = transform.R` (có thể viết thêm hàm hỗ trợ).

Sau đó mở file URDF, ví dụ:

`my_robot/urdf/walle_cam_lidar_calib_example.urdf.xacro`

và sửa joint:

```xml
<joint name="lidar_mount" type="fixed">
  <parent link="camera_link"/>
  <child  link="lidar_link"/>
  <origin xyz="tx ty tz" rpy="roll pitch yaw"/>
</joint>
```

- `xyz` = `t_x t_y t_z`.
- `rpy` = góc quay tương ứng với `R_est` (thường rất nhỏ nếu bạn lắp khá thẳng).

Khi chạy `robot_state_publisher` với URDF này, TF tree của robot sẽ phản ánh đúng quan hệ hình học giữa camera và LiDAR → từ đó bạn có thể so sánh khoảng cách, tính sai số, hoặc dùng cho navigation/SLAM.

---

## 6. Gợi ý cách học/nhớ nhanh

- Hãy nhớ: **Kabsch = xoay + tịnh tiến để hai đám mây điểm khớp nhau nhất.**
- Trực giác:
  1. Dời hai đám mây sao cho tâm của chúng trùng gốc.
  2. Tìm phép quay làm chúng khớp tốt nhất (dùng SVD).
  3. Dời lại để tâm đúng vị trí ban đầu → ra tịnh tiến.
- Phần toán ma trận (SVD) đã gói trong numpy, bạn chỉ cần hiểu ý nghĩa và dùng đúng đầu vào/đầu ra.

---

## 7. Checklist thực hành từng bước

1. **Chuẩn bị phần cứng**
  - Lắp cố định LiDAR và camera lên robot (không xê dịch trong quá trình đo).
  - Đặt robot cách tường/phông nền vài mét để có khoảng rộng đặt marker.

2. **Chuẩn bị marker và môi trường**
  - In 1–2 ArUco marker (hoặc vật mốc rõ ràng) dán trên tấm bìa phẳng.
  - Đặt marker trong vùng mà **cả camera và LiDAR đều “nhìn thấy” được**.
  - Thay đổi vị trí marker: gần/xa, trái/phải, cao/thấp, mỗi vị trí chụp vài lần.

3. **Thu thập dữ liệu cho `points_C` (hệ camera)**
  - Viết (hoặc dùng sẵn) node ROS2 nhận ảnh + depth từ D435i.
  - Phát hiện ArUco → tính tọa độ 3D tâm marker trong hệ `camera_link`.
  - Lưu mỗi mẫu thành một điểm `p_C^{(i)} = (x_C^{(i)}, y_C^{(i)}, z_C^{(i)})`.

4. **Thu thập dữ liệu cho `points_L` (hệ LiDAR)**
  - Từ scan LiDAR, trích cụm điểm tương ứng với marker (tường/plane chứa marker).
  - Lấy tâm hình học (centroid) cụm này: `p_L^{(i)} = (x_L^{(i)}, y_L^{(i)}, z_L^{(i)})`.
  - Với LiDAR 2D: đặt luôn `z_L^{(i)} = 0`.

5. **Tạo mảng dữ liệu và chạy hiệu chỉnh**
  - Gom các điểm đã thu thành hai mảng:
    - `points_C = [p_C^{(1)}, ..., p_C^{(N)}]`.
    - `points_L = [p_L^{(1)}, ..., p_L^{(N)}]`.
  - Dùng Python (vd. file `cam_lidar_calib_example.py`) gọi:

    ```python
    transform, rmse = kabsch_align(points_L, points_C)
    ```

  - Kiểm tra `rmse` đủ nhỏ (vài mm–cm).

6. **Ghi kết quả vào URDF/TF**
  - Ghi `transform.t` vào `origin xyz="tx ty tz"` của joint giữa `camera_link` và `lidar_link`.
  - Nếu cần quay: tính `roll, pitch, yaw` từ `transform.R` và ghi vào `rpy`.

7. **Kiểm tra lại bằng RViz**
  - Chạy robot với URDF mới, mở RViz, add:
    - LiDAR scan.
    - PointCloud/Depth từ camera.
  - Di chuyển marker và quan sát: 
    - Vị trí marker trong hai nguồn dữ liệu phải **trùng nhau (hoặc rất gần)**.
  - Nếu lệch nhiều: quay lại bước 2–5, thu thêm điểm và hiệu chỉnh lại.
