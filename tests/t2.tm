*:run [], []
  0: LDA 7, 3(7)
  1: LDC 2, 4(0)
  2: ADD 2, 2, 2
  3:  ST 2, 1(0)
  4: LDA 7, 1(7)
  5: LDC 4, 4(0)
  6: LDA 7, 2(7)
  7: SUB 1, 4, 2
  8:  ST 1, 2(0)
  9: OUT 0, 0, 0
 10: JNE 0, 9(0)
 11: HALT 7,7,7
