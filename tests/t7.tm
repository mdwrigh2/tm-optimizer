*:run [], []
*:run [], [-1]
 .DATA 10
  0:  LD 1, 1(0)
  1: JLE 1, 5(7)
  2: LDC 2, 5(0)
  3: OUT 2, 2, 2
  4: OUTNL 1,1,1
  5: LDA 1,-1(1)
  6: LDA 7,-6(7)
  7: HALT 0,0,0
