"""Exact template builders extracted from the author scripts; no API access."""

def get_prompt_emb0(row):
    return f"Chemical name: {row['name']}.\nUsed as a corrosion inhibitor."

def get_prompt_emb1(row):
    return (f"Chemical name: {row['name']}.\n"
            f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Used as a corrosion inhibitor.")

def get_prompt_emb2(row):
    return (f"Chemical name: {row['name']}.\n"
            f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
            f"Used as a corrosion inhibitor.")

def prompt_A(row):
    return (f"Chemical name: {row['name']}.\n"
            f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
            f"Van der Waals surface descriptor P_VSA_MR_5: {row['P_VSA_MR_5']}.\n"
            f"Used as a corrosion inhibitor.")

def get_prompt_emb4(row):
    return (f"Chemical name: {row['name']}.\n"
            f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
            f"Van der Waals surface descriptor P_VSA_MR_5: {row['P_VSA_MR_5']}.\n"
            f"CATS3D descriptor: {row['CATS3D_02_AP']}.\n"
            f"Used as a corrosion inhibitor.")

def get_prompt_emb5(row):
    return (f"Chemical name: {row['name']}.\n"
            f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
            f"Van der Waals surface descriptor P_VSA_MR_5: {row['P_VSA_MR_5']}.\n"
            f"CATS3D descriptor: {row['CATS3D_02_AP']}.\n"
            f"3D-MoRSE descriptor: {row['Mor04m']}.\n"
            f"Used as a corrosion inhibitor.")

def prompt_smiles(row):
    return (
        f"Chemical name: {row['name']}.\n"
        f"SMILES: {row['isomeric_smiles']}.\n"
        f"LUMO energy: {row['LUMO / eV']} eV.\n"
        f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
        f"Van der Waals surface descriptor P_VSA_MR_5: {row['P_VSA_MR_5']}.\n"
        f"Used as a corrosion inhibitor."
    )

def prompt_B(row):
    return (f"This document defines the structural and electronic profile of the organic corrosion inhibitor "
            f"'{row['name']}'. The LUMO energy is {row['LUMO / eV']} eV, describing its electron-accepting "
            f"characteristics. The directional accessibility descriptor E1p is {row['E1p']}, characterizing "
            f"the directional accessibility of the molecular structure. The van der Waals surface descriptor "
            f"P_VSA_MR_5 is {row['P_VSA_MR_5']}. These descriptors characterize molecular features relevant "
            f"to corrosion inhibition.")

def prompt_C(row):
    return (f"Target compound {row['name']} is evaluated as a corrosion inhibitor. The LUMO energy is "
            f"{row['LUMO / eV']} eV, providing information on electron-accepting characteristics. The "
            f"directional accessibility descriptor E1p is {row['E1p']}, characterizing the directional "
            f"accessibility of the molecular structure. The van der Waals surface descriptor P_VSA_MR_5 is "
            f"{row['P_VSA_MR_5']}. These descriptors characterize electronic and molecular structural "
            f"features relevant to corrosion inhibition.")

def prompt_D(row):
    return (f"LUMO={row['LUMO / eV']} "
            f"E1p={row['E1p']} "
            f"P_VSA_MR_5={row['P_VSA_MR_5']}"
)

def prompt_E(row):

    return (f"Chemical name: {row['name']}.\n"
            f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
            f"Van der Waals surface descriptor P_VSA_MR_5: {row['P_VSA_MR_5']}.\n"
)

def prompt_F(row):
    return (f"LUMO energy: {row['LUMO / eV']} eV.\n"
            f"Directional accessibility descriptor E1p: {row['E1p']}.\n"
            f"Van der Waals surface descriptor P_VSA_MR_5: {row['P_VSA_MR_5']}.\n"
            f"Used as a corrosion inhibitor."
)


ED_PROMPTS = [get_prompt_emb0, get_prompt_emb1, get_prompt_emb2, prompt_A, get_prompt_emb4, get_prompt_emb5]
TEMPLATES = {'A': prompt_A, 'B': prompt_B, 'C': prompt_C, 'D': prompt_D, 'E': prompt_E, 'F': prompt_F}

def texts(frame, key):
    if key.startswith('qwen_ed'):
        function = ED_PROMPTS[int(key[-1])]
    elif key == 'qwen_smiles':
        function = prompt_smiles
    elif key.startswith('qwen_prompt_'):
        function = TEMPLATES[key[-1]]
    else:
        raise ValueError('No Qwen template defined for '+key)
    # Matches the original get_embedding(): replace newlines with spaces.
    return [function(row).replace('\n', ' ') for _, row in frame.iterrows()]
