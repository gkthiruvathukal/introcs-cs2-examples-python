import math
import pytest

from data_structures.unsigned_int import UnsignedInt, render_visualization, VALID_SIZES


# ── construction ──────────────────────────────────────────────────────────────

def test_default_is_8bit_zero():
    u = UnsignedInt()
    assert u.size == 8
    assert u.value == 0


def test_valid_sizes_accepted():
    for size in VALID_SIZES:
        assert UnsignedInt(size=size).size == size


def test_invalid_size_raises():
    with pytest.raises(ValueError, match="Size must be one of"):
        UnsignedInt(size=7)


def test_value_at_max():
    u = UnsignedInt(size=8, value=255)
    assert u.value == 255


def test_value_above_max_raises():
    with pytest.raises(ValueError):
        UnsignedInt(size=8, value=256)


def test_negative_value_raises():
    with pytest.raises(ValueError):
        UnsignedInt(size=8, value=-1)


# ── set_value ─────────────────────────────────────────────────────────────────

def test_set_value_round_trips():
    u = UnsignedInt(size=8)
    u.set_value(85)
    assert u.value == 85


# ── bit operations ────────────────────────────────────────────────────────────

def test_set_bit_lsb():
    u = UnsignedInt(size=8, value=0)
    u.set_bit(0)
    assert u.value == 1


def test_reset_bit():
    u = UnsignedInt(size=8, value=0b11111111)
    u.reset_bit(0)
    assert u.value == 0b11111110


def test_toggle_bit():
    u = UnsignedInt(size=8, value=0)
    u.toggle_bit(3)
    assert u.value == 8
    u.toggle_bit(3)
    assert u.value == 0


def test_get_bit():
    u = UnsignedInt(size=8, value=0b10100101)
    assert u.get_bit(0) == 1
    assert u.get_bit(1) == 0
    assert u.get_bit(7) == 1


def test_bit_pos_out_of_range_raises():
    u = UnsignedInt(size=8)
    with pytest.raises(ValueError):
        u.set_bit(8)
    with pytest.raises(ValueError):
        u.reset_bit(-1)


# ── bit_list ─────────────────────────────────────────────────────────────────

def test_bit_list_byte_85():
    u = UnsignedInt(size=8, value=85)  # 0b01010101
    assert u.bit_list() == [0, 1, 0, 1, 0, 1, 0, 1]


def test_bit_list_length_equals_size():
    for size in VALID_SIZES:
        u = UnsignedInt(size=size, value=0)
        assert len(u.bit_list()) == size


# ── octal groups ──────────────────────────────────────────────────────────────

def test_octal_groups_byte_85():
    u = UnsignedInt(size=8, value=85)  # oct 125
    assert u.octal_groups() == [1, 2, 5]


def test_octal_groups_nibble_value_15():
    u = UnsignedInt(size=4, value=15)  # 0b1111 = octal 17
    assert u.octal_groups() == [1, 7]


def test_phantom_bit_count_byte():
    assert UnsignedInt(size=8).phantom_bit_count() == 1  # ceil(8/3)*3 - 8 = 9 - 8 = 1


def test_phantom_bit_count_nibble():
    assert UnsignedInt(size=4).phantom_bit_count() == 2  # ceil(4/3)*3 - 4 = 6 - 4 = 2


def test_phantom_bit_count_16bit():
    assert UnsignedInt(size=16).phantom_bit_count() == 2  # ceil(16/3)*3 - 16 = 18 - 16 = 2


def test_display_bit_width():
    assert UnsignedInt(size=8).display_bit_width() == 9
    assert UnsignedInt(size=4).display_bit_width() == 6
    assert UnsignedInt(size=16).display_bit_width() == 18


def test_set_octal_group_rightmost():
    u = UnsignedInt(size=8, value=0)
    u.set_octal_group(0, 5)  # rightmost group → bits 0,1,2 = 101 = 5
    assert u.value == 5
    assert u.octal_groups()[2] == 5


def test_set_octal_group_middle():
    u = UnsignedInt(size=8, value=0)
    u.set_octal_group(1, 3)  # middle group → bits 3,4,5 = 011 = 3
    assert u.value == 3 << 3


def test_set_octal_group_msb_overflow_raises():
    u = UnsignedInt(size=8, value=0)
    # MSB group has 1 phantom bit, so only 2 real bits → max digit = 2^2-1 = 3
    with pytest.raises(ValueError, match="MSB octal group"):
        u.set_octal_group(2, 4)  # 4 needs 3 bits; phantom bit would overflow


def test_set_octal_group_out_of_range_raises():
    u = UnsignedInt(size=8, value=0)
    with pytest.raises(ValueError):
        u.set_octal_group(3, 1)


# ── hex groups ────────────────────────────────────────────────────────────────

def test_hex_groups_byte_85():
    u = UnsignedInt(size=8, value=85)  # 0x55
    assert u.hex_groups() == [5, 5]


def test_set_hex_group_rightmost():
    u = UnsignedInt(size=8, value=0)
    u.set_hex_group(0, 0xA)
    assert u.value == 0x0A
    assert u.hex_groups()[1] == 0xA


def test_set_hex_group_msb():
    u = UnsignedInt(size=8, value=0)
    u.set_hex_group(1, 0xF)
    assert u.value == 0xF0


def test_set_hex_group_out_of_range_raises():
    u = UnsignedInt(size=8)
    with pytest.raises(ValueError):
        u.set_hex_group(2, 0)
    with pytest.raises(ValueError):
        u.set_hex_group(0, 16)


# ── clear ─────────────────────────────────────────────────────────────────────

def test_clear_resets_to_zero():
    u = UnsignedInt(size=8, value=255)
    u.clear()
    assert u.value == 0


# ── string representations ────────────────────────────────────────────────────

def test_to_bin():
    u = UnsignedInt(size=8, value=85)
    assert u.to_bin() == "0b01010101"


def test_to_oct():
    u = UnsignedInt(size=8, value=85)
    assert u.to_oct() == "0o125"


def test_to_hex():
    u = UnsignedInt(size=8, value=85)
    assert u.to_hex() == "0x55"


def test_to_hex_zero_padded():
    u = UnsignedInt(size=16, value=0x0A0B)
    assert u.to_hex() == "0x0A0B"


# ── shift left ───────────────────────────────────────────────────────────────

def test_shift_left_basic():
    u = UnsignedInt(size=8, value=0b00000001)
    lost = u.shift_left(1)
    assert u.value == 0b00000010
    assert lost == 0


def test_shift_left_overflow():
    u = UnsignedInt(size=8, value=0b10000001)
    lost = u.shift_left(1)
    assert u.value == 0b00000010
    assert lost == 1  # MSB was 1


def test_shift_left_by_full_size_clears_value():
    u = UnsignedInt(size=8, value=0xFF)
    lost = u.shift_left(8)
    assert u.value == 0
    assert lost == 0xFF


def test_shift_left_by_zero_is_noop():
    u = UnsignedInt(size=8, value=42)
    lost = u.shift_left(0)
    assert u.value == 42
    assert lost == 0


def test_shift_left_negative_raises():
    u = UnsignedInt(size=8)
    with pytest.raises(ValueError):
        u.shift_left(-1)


# ── shift right ───────────────────────────────────────────────────────────────

def test_shift_right_basic():
    u = UnsignedInt(size=8, value=0b10000000)
    u.shift_right(1)
    assert u.value == 0b01000000


def test_shift_right_fills_zeros():
    u = UnsignedInt(size=8, value=0xFF)
    u.shift_right(4)
    assert u.value == 0x0F


def test_shift_right_by_full_size_clears():
    u = UnsignedInt(size=8, value=0xFF)
    u.shift_right(8)
    assert u.value == 0


# ── rotate ────────────────────────────────────────────────────────────────────

def test_rotate_left_basic():
    u = UnsignedInt(size=8, value=0b10000001)
    u.rotate_left(1)
    assert u.value == 0b00000011


def test_rotate_right_basic():
    u = UnsignedInt(size=8, value=0b10000001)
    u.rotate_right(1)
    assert u.value == 0b11000000


def test_rotate_left_full_rotation_is_identity():
    u = UnsignedInt(size=8, value=0b11001010)
    original = u.value
    u.rotate_left(8)
    assert u.value == original


def test_rotate_right_full_rotation_is_identity():
    u = UnsignedInt(size=8, value=0b11001010)
    original = u.value
    u.rotate_right(16)  # 2 full rotations
    assert u.value == original


# ── complement ────────────────────────────────────────────────────────────────

def test_complement_flips_all_bits():
    u = UnsignedInt(size=8, value=0b00000000)
    u.complement()
    assert u.value == 0xFF


def test_complement_twice_is_identity():
    u = UnsignedInt(size=8, value=85)
    original = u.value
    u.complement()
    u.complement()
    assert u.value == original


def test_complement_stays_within_size():
    u = UnsignedInt(size=4, value=0b0000)
    u.complement()
    assert u.value == 0b1111  # only 4 bits flipped, not 8


# ── bitwise and / or / xor ────────────────────────────────────────────────────

def test_bitwise_and():
    u = UnsignedInt(size=8, value=0b11001100)
    u.bitwise_and(0b10101010)
    assert u.value == 0b10001000


def test_bitwise_or():
    u = UnsignedInt(size=8, value=0b11001100)
    u.bitwise_or(0b00110011)
    assert u.value == 0b11111111


def test_bitwise_xor():
    u = UnsignedInt(size=8, value=0b11001100)
    u.bitwise_xor(0b11001100)
    assert u.value == 0


def test_bitwise_and_with_zero_clears():
    u = UnsignedInt(size=8, value=0xFF)
    u.bitwise_and(0)
    assert u.value == 0


def test_bitwise_or_with_mask_sets_all():
    u = UnsignedInt(size=8, value=0)
    u.bitwise_or(0xFF)
    assert u.value == 0xFF


def test_bitwise_operand_out_of_range_raises():
    u = UnsignedInt(size=8)
    with pytest.raises(ValueError):
        u.bitwise_and(256)
    with pytest.raises(ValueError):
        u.bitwise_or(-1)


# ── render_visualization ──────────────────────────────────────────────────────

def _total_row_width(uint: UnsignedInt) -> int:
    n = uint.display_bit_width()
    return 1 + n * 4  # ┌ + n*(inner+border)


def test_render_visualization_rows_all_same_width_byte():
    u = UnsignedInt(size=8, value=85)
    vis = render_visualization(u)
    lines = vis.splitlines()
    # Every box row (border or data) should be exactly 37 chars for 8-bit.
    # Expected: 1 + display_bit_width*4 = 1 + 9*4 = 37
    box_lines = [l for l in lines if l.startswith("┌") or l.startswith("│") or l.startswith("└")]
    expected = 37
    for line in box_lines:
        assert len(line) == expected, f"Row width {len(line)} != {expected}: {line!r}"


def test_render_visualization_contains_phantom_dot():
    u = UnsignedInt(size=8, value=0)
    vis = render_visualization(u)
    assert "·" in vis


def test_render_visualization_byte_85_binary_row():
    u = UnsignedInt(size=8, value=85)  # 0b01010101
    vis = render_visualization(u)
    # The binary data row contains the bit pattern with phantom
    lines = vis.splitlines()
    bin_data = next(l for l in lines if "·" in l and "│" in l)
    assert "· " in bin_data  # phantom bit
    assert " 0 " in bin_data
    assert " 1 " in bin_data


def test_render_visualization_hex_row_shows_55():
    u = UnsignedInt(size=8, value=85)  # hex 0x55
    vis = render_visualization(u)
    lines = vis.splitlines()
    hex_label_idx = next(i for i, l in enumerate(lines) if l == "Hex")
    hex_data_row = lines[hex_label_idx + 2]
    assert hex_data_row.count("5") == 2


def test_render_visualization_octal_row_shows_125():
    u = UnsignedInt(size=8, value=85)  # oct 125
    vis = render_visualization(u)
    lines = vis.splitlines()
    # Octal data row: no phantom, has numbers 1, 2, 5
    oct_label_idx = next(i for i, l in enumerate(lines) if l == "Octal")
    oct_data_row = lines[oct_label_idx + 2]  # top, data, bot
    assert "1" in oct_data_row
    assert "2" in oct_data_row
    assert "5" in oct_data_row


def test_render_visualization_nibble_row_widths():
    u = UnsignedInt(size=4, value=0)
    vis = render_visualization(u)
    lines = vis.splitlines()
    # Expected width for 4-bit: display_bit_width=6, total=1+6*4=25
    box_rows = [l for l in lines if "┌" in l or ("│" in l and "─" not in l) or "└" in l]
    # Just check binary row width
    bin_top = lines[1]
    assert len(bin_top) == 25
