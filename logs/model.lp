\ Model LargeSI
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  X[0] + X[1] + X[2] + X[3] + X[4] + X[5] + X[6] + X[7] + X[8] + X[9]
   + X[10] + X[11] + X[12] + X[13]
Subject To
 Constraint_on_starting_seed: Z[0] + Z[1] + Z[2] + Z[3] + Z[4] + Z[5]
   + Z[6] + Z[7] + Z[8] + Z[9] + Z[10] + Z[11] + Z[12] + Z[13] <= 2
 R1: X[0] <= 0
 R2: X[1] <= 0
 R3: X[2] <= 0
 R4: X[3] <= 0
 R5: X[4] <= 0
 R6: X[5] <= 0
 R7: X[6] <= 0
 R8: X[7] <= 0
 R9: X[8] - Z[2] <= 0
 R10: X[9] - Z[4] <= 0
 R11: X[10] - Z[4] <= 0
 R12: X[11] <= 0
 R13: X[12] <= 0
 R14: X[13] <= 0
Bounds
 X[0] <= 1
 X[1] <= 1
 X[2] <= 1
 X[3] <= 1
 X[4] <= 1
 X[5] <= 1
 X[6] <= 1
 X[7] <= 1
 X[8] <= 1
 X[9] <= 1
 X[10] <= 1
 X[11] <= 1
 X[12] <= 1
 X[13] <= 1
 Z[0] <= 1
 Z[1] <= 1
 Z[2] <= 1
 Z[3] <= 1
 Z[4] <= 1
 Z[5] <= 1
 Z[6] <= 1
 Z[7] <= 1
 Z[8] <= 1
 Z[9] <= 1
 Z[10] <= 1
 Z[11] <= 1
 Z[12] <= 1
 Z[13] <= 1
Generals
 X[0] X[1] X[2] X[3] X[4] X[5] X[6] X[7] X[8] X[9] X[10] X[11] X[12] X[13]
 Z[0] Z[1] Z[2] Z[3] Z[4] Z[5] Z[6] Z[7] Z[8] Z[9] Z[10] Z[11] Z[12] Z[13]
End
