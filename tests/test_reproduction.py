"""Checks for cache integrity, optional API isolation and DS15-label separation."""
import sys, unittest, tempfile, shutil, json
from pathlib import Path
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from hrlcor import data
from hrlcor.representations import build


class ReproductionChecks(unittest.TestCase):
    def test_supplied_caches_need_no_api(self):
        for key in ['qwen_ed0','qwen_ed3','qwen_smiles','bge_m3','scibert']:
            self.assertEqual(len(data.load_embedding(key)),75)
        self.assertNotIn('hrlcor.optional_api',sys.modules)

    def test_changed_data_order_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            shutil.copytree(ROOT/'data',target/'data')
            path=target/'data/raw/dataset.csv'
            import pandas as pd
            pd.read_csv(path).iloc[::-1].to_csv(path,index=False)
            with patch.object(data,'ROOT',target):
                with self.assertRaisesRegex(ValueError,'changed'):
                    data.load_dataset()

    def test_heldout_labels_do_not_change_representation(self):
        frame=data.load_dataset()
        changed=frame.copy();changed.loc[60:,'ie_ze41']=99999
        original=build(frame,structural=None)
        modified=build(changed,structural=None)
        np.testing.assert_array_equal(original.train,modified.train)
        np.testing.assert_array_equal(original.test,modified.test)
        self.assertEqual(original.dimensions,(0,37,2))

    def test_missing_cache_does_not_start_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);(target/'data/raw').mkdir(parents=True)
            shutil.copy2(ROOT/'data/raw/dataset.csv',target/'data/raw/dataset.csv')
            shutil.copy2(ROOT/'data/manifest.json',target/'data/manifest.json')
            with patch.object(data,'ROOT',target):
                with self.assertRaises(FileNotFoundError):data.load_embedding('qwen_ed3')
        self.assertNotIn('hrlcor.optional_api',sys.modules)

    def test_structural_csv_preserves_original_float32_values(self):
        import pandas as pd
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);(target/'data/raw').mkdir(parents=True)
            (target/'data/embeddings').mkdir()
            shutil.copy2(ROOT/'data/raw/dataset.csv',target/'data/raw/dataset.csv')
            shutil.copy2(ROOT/'data/manifest.json',target/'data/manifest.json')
            values=np.random.default_rng(42).normal(size=(75,512)).astype('float32')
            path=target/'data/embeddings/unimol.csv'
            pd.DataFrame(values.astype('float64')).to_csv(path,index=False,float_format='%.17g')
            path.with_suffix('.json').write_text(json.dumps({'dataset_sha256':data.digest(target/'data/raw/dataset.csv'),
                'csv_sha256':data.digest(path),'original_dtype':'float32'}))
            with patch.object(data,'ROOT',target):
                restored=data.load_embedding('unimol')
            self.assertEqual(restored.dtype,values.dtype)
            np.testing.assert_array_equal(restored,values)


if __name__=='__main__':unittest.main()
