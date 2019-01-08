Website TSULOTT2 có 5 routes:

- Home: Hiển thị số tiền và item hiện có
- Ticket: Tạo ticket với 2 parameters: number (0 - 50) và bet
- Lott: Điền ticket để quay lotto, trúng thì được x2 tiền bet, trượt thì mất tiền bet
- Market: Mua item: Tsu (500), Flower (500), Source (2000), Flag (1337000000)
- Reset: Khởi tạo lại session

Ta có một nhận xét là không gian mẫu của lotto khá nhỏ (0 - 50) nên ta có thể bet bừa và hy vọng sẽ trúng vào một lúc nào đó, ta sẽ có được 2000 để mua source.
Sau khi mua được source, ta bắt đầu nghiên cứu. Đầu tiên ta xem phần xử lý tạo ticket (`buy_ticket` file `src.py`). Ta rút ra được 2 điều:

- Ticket có dạng `number=%s;bet=%s;session=%s`, được encrypt bằng thuật toán AES mode CBC với block size = 16
- Hàm này chỉ check string `bet` có chứa toàn số hay không => có thể truyền một số bất kỳ

Tiếp tục đến phần quay lotto (`lott` file `src.py`). Ta lại rút ra vài điều:

- `bet` không được chứa '+' hoặc '-'
- `bet` sẽ bị strip khoảng trắng ở đầu đuôi trước khi truyền vào `check_bet`
- `check_bet` kiểm tra length của số truyền vào (kiểu `string`) bằng cách thử xem có convert được từng ký tự sang `int` hay không, nếu không convert được thì dừng
- Sau khi kiểm tra length, `check_bet` sẽ so sánh số tiền hiện có với số tiền truyền vào bằng cách so sánh từng ký tự từ trái sang phải
- Sau khi pass `check_bet`, kiểm tra `number`, nếu trùng với `jackpot` thì người chơi thắng, không thì người chơi thua (tăng / giảm `money` một lượng `int(bet)`)

Từ những nhận xét trên, ta thấy rằng: Muốn bet được số tiền lớn hơn số tiền hiện tại đang có thì phải pass được `check_bet`, đồng thời `int(bet)` phải ra được một số lớn.
Đọc changelog python 3.6, hàm `int()` chấp nhận dấu `_` trong string để nhìn số dễ dàng hơn và nó sẽ bị ignore khi convert sang `int` => Có thể dùng để lừa phần check length của `check_bet`.
Vấn đề là lúc tạo ticket, ta chỉ truyền vào được số. Nhưng ticket không được lưu trên server => ta có thể fake ticket.
Như đã nói ở trên, ticket được mã hóa AES-CBC với blocksize 16. Quá trình decrypt diễn ra như sau:

```
// P: plaintext blocks, C: ciphertext blocks, IV: initialization vector, D: decrypt function
P[0] = D(C[0]) ^ IV
P[i] = D(C[i]) ^ C[i - 1]
```

Với mode CBC, ta có thể sử dụng **Byte flipping attack** để thay đổi dữ liệu. Biết format của ticket, ta tiến hành tạo ticket với `number = 1` và `bet = 100000000000000`. Chia data theo block size:

```
number=1;bet=100
000000000000;ses
sion=?????
```

Mình chọn tấn công vào byte cuối cùng của block đầu tiên, thay đổi `0` thành `_` => `IV[15] ^= '0' ^ '_'`. Plaintext sau khi decrypt sẽ trở thành:

```
number=1;bet=10_000000000000;session=?????
```

Giờ ta tiếp tục bet bừa và chờ đến khi trúng thì mua flag (file `attack.py`). Flag của challenge là:

```
TetCTF{__Pyth0n__3___hahahah4hahaha__}
```
