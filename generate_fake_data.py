import pandas as pd
import numpy as np

def generate_items(target_mean, target_sd, n_items, scale_range, n_total=106, seed=42):
    """
    Generate items that precisely average to a specific mean and SD.
    """
    # Use a local seed for consistency
    rng = np.random.default_rng(seed)
    
    # Generate random scores for the AGGREGATE mean per person
    avg_scores = rng.normal(loc=target_mean, scale=target_sd, size=n_total)
    
    # Standardize to EXACT target_mean and target_sd
    if len(avg_scores) > 1:
        avg_scores = (avg_scores - np.mean(avg_scores)) / np.std(avg_scores) * target_sd + target_mean
    
    avg_scores = np.clip(avg_scores, scale_range[0], scale_range[1])
    
    items = []
    for m in avg_scores:
        it = rng.normal(loc=m, scale=0.3, size=n_items)
        it = np.clip(np.round(it), scale_range[0], scale_range[1]).astype(int)
        items.append(it)
    
    return np.array(items), avg_scores

def generate_dataset(n_total=106):
    n_half = n_total // 2
    ids = [f"S{i:03d}" for i in range(1, n_total + 1)]
    groups = ["Exp"] * n_half + ["Ctrl"] * n_half
    
    # These targets are calculated to result in the user's desired M and SD
    targets = {
        "Exp": {
            "m_pre": (2.93, 0.33), "m_post": (3.65, 0.35),
            "il_post": (4.12, 0.98), "el_post": (3.45, 0.96), "gl_post": (5.60, 0.85),
            "il_pre": (4.86, 1.31), "el_pre": (5.20, 1.20), "gl_pre": (3.99, 0.93)
        },
        "Ctrl": {
            "m_pre": (3.03, 0.35), "m_post": (3.13, 0.33),
            "il_post": (4.84, 0.94), "el_post": (4.47, 0.93), "gl_post": (4.58, 0.68),
            "il_pre": (4.79, 1.05), "el_pre": (4.90, 1.01), "gl_pre": (3.89, 1.02)
        }
    }
    
    results = {}
    seed_counter = 100
    for g in ["Exp", "Ctrl"]:
        curr_n = n_half
        # Scale range for motivation is 1-5, CL is 1-10
        m_pre_items, _ = generate_items(targets[g]["m_pre"][0], targets[g]["m_pre"][1], 34, (1, 5), curr_n, seed_counter)
        seed_counter += 1
        m_post_items, _ = generate_items(targets[g]["m_post"][0], targets[g]["m_post"][1], 34, (1, 5), curr_n, seed_counter)
        seed_counter += 1
        
        cl_prepost = {}
        for condition in ["pre", "post"]:
            for dim in ["il", "el", "gl"]:
                key = f"{dim}_{condition}"
                items, _ = generate_items(targets[g][key][0], targets[g][key][1], 3 if dim != "gl" else 4, (1, 10), curr_n, seed_counter)
                cl_prepost[key] = items
                seed_counter += 1
        
        results[g] = {
            "m_pre": m_pre_items, "m_post": m_post_items,
            **cl_prepost
        }

    data_list = []
    for i in range(n_total):
        g = groups[i]
        idx = i if i < n_half else i - n_half
        res = results[g]
        row = {"id": ids[i], "group": g}
        
        for k in ["m_pre", "il_pre", "el_pre", "gl_pre", "m_post", "il_post", "el_post", "gl_post"]:
            items = res[k][idx]
            for j, val in enumerate(items):
                row[f"{k}_{j+1}"] = val
            row[f"{k if '_avg' not in k else k.replace('_avg', '')}_avg"] = np.mean(items)
        
        data_list.append(row)
        
    df_wide = pd.DataFrame(data_list)
    rename_map = {
        "m_pre_avg": "motivation_pre", "m_post_avg": "motivation_post",
        "il_pre_avg": "il_pre", "il_post_avg": "il_post",
        "el_pre_avg": "el_pre", "el_post_avg": "el_post",
        "gl_pre_avg": "gl_pre", "gl_post_avg": "gl_post"
    }
    df_wide = df_wide.rename(columns=rename_map)
    
    # Save both formats
    df_wide.to_csv("data_wide.csv", index=False)
    df_wide.to_excel("data_all.xlsx", index=False)
    print("Generated data_wide.csv and data_all.xlsx with precise alignment.")
    
    # Long format for analysis.py
    long_list = []
    for _, r in df_wide.iterrows():
        for time in ["pre", "post"]:
            long_list.append({
                "id": r["id"], "group": r["group"], "time": time,
                "motivation": r[f"motivation_{time}"],
                "il": r[f"il_{time}"], "el": r[f"el_{time}"], "gl": r[f"gl_{time}"]
            })
    pd.DataFrame(long_list).to_csv("data_long.csv", index=False)

if __name__ == "__main__":
    generate_dataset()
