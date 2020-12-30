// Generated by KLFC 1.5.6
// https://github.com/39aldo39/klfc

#include "unimap_trans.h"
#include "action_util.h"
#include "action_layer.h"

enum function_id {
    F_MODIFIER,
};

enum macro_id {
    LIG__numbersign_,
};

enum modifier_id {
    MOD_SHIFT,
    MOD_SHIFT_L,
    MOD_SHIFT_R,
};

#define AC_FN0 ACTION_MACRO(LIG__numbersign_)
#define AC_FN1 ACTION_FUNCTION_OPT(F_MODIFIER, MOD_SHIFT_L)
#define AC_FN2 ACTION_FUNCTION_OPT(F_MODIFIER, MOD_SHIFT_R)

#ifdef KEYMAP_SECTION_ENABLE
const action_t actionmaps[][UNIMAP_ROWS][UNIMAP_COLS] __attribute__ ((section (".keymap.keymaps"))) = {
#else
const action_t actionmaps[][UNIMAP_ROWS][UNIMAP_COLS] PROGMEM = {
#endif
    // None
    [0] = UNIMAP(
               F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F23, F24,
     ESC,       F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12,          PSCR,SLCK,PAUS,         VOLD,VOLU,MUTE,
     GRV,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0,MINS, EQL,JYEN,BSPC,      INS,HOME,PGUP,    NLCK,PSLS,PAST,PMNS,
     TAB,   Q,   W,   D,   F,   G,   Y,   U,   K,   P,SCLN,LBRC,RBRC,      FN0,      DEL, END,PGDN,      P7,  P8,  P9,PPLS,
    CAPS,   A,   S,   E,   R,   T,   H,   N,   I,   O,   L,QUOT,     NUHS, ENT,                          P4,  P5,  P6,PCMM,
     FN1,BSLS,   Z,   X,   C,   V,   B,   J,   M,COMM, DOT,SLSH,       RO, FN2,            UP,           P1,  P2,  P3,PENT,
    LCTL,LGUI,LALT,MHEN,           SPC,          HENK,KANA,RALT,RGUI, APP,RCTL,     LEFT,DOWN,RGHT,      P0,     PDOT,PEQL
    ),
    // Shift
    [1] = UNIMAP(
              TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,
    TRNS,     TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,          TRNS,TRNS,TRNS,         TRNS,TRNS,TRNS,
      NO,TRNS,QUOT,  NO,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,     TRNS,TRNS,TRNS,    TRNS,TRNS,TRNS,TRNS,
    TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,      GRV,     TRNS,TRNS,TRNS,    TRNS,TRNS,TRNS,TRNS,
    TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,   2,     TRNS,TRNS,                        TRNS,TRNS,TRNS,TRNS,
    TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,     TRNS,TRNS,          TRNS,         TRNS,TRNS,TRNS,TRNS,
    TRNS,TRNS,TRNS,TRNS,          TRNS,          TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,     TRNS,TRNS,TRNS,    TRNS,     TRNS,TRNS
    ),
};

const macro_t *action_get_macro(keyrecord_t *record, uint8_t id, uint8_t opt) {
    switch (id) {
        case LIG__numbersign_:
            return record->event.pressed ?
                   MACRO(SM(), CM(), D(LSFT), T(3), U(LSFT), RM(), END) :
                   MACRO_NONE;
    }
    return MACRO_NONE;
}

#define MOD_SHIFT_MASK (MOD_BIT(KC_LSFT)|MOD_BIT(KC_RSFT))

uint8_t vmods = 0;

const uint8_t layer_states[] = {
    0x1, // None
    0x3, // Shift
};

void action_function(keyrecord_t *record, uint8_t id, uint8_t opt) {
    uint8_t pressed = record->event.pressed;
    switch (id) {
        case F_MODIFIER:
            // Set the new modifier
            switch (opt) {
                case MOD_SHIFT: pressed ? add_key(KC_LSFT) : del_key(KC_LSFT); break;
                case MOD_SHIFT_L: pressed ? add_key(KC_LSFT) : del_key(KC_LSFT); break;
                case MOD_SHIFT_R: pressed ? add_key(KC_RSFT) : del_key(KC_RSFT); break;
            }

            // Update the layer
            uint8_t mods = get_mods();
            uint8_t layer_index = 0;
            layer_index |= mods & MOD_SHIFT_MASK ? 1 : 0;
            layer_index |= vmods << 1;
            layer_clear();
            layer_or(layer_states[layer_index]);
            break;
    }
}
