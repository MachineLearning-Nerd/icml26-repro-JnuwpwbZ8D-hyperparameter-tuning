# C6 limitations

The source does not typeset `alpha_i>=0` even though it calls the coordinates
regularization weights and its dual proof requires nonnegative box radii. The
certificate is therefore MEDIUM confidence rather than silently testing
negative weights. The priority and exact minimal region count are not claimed.
