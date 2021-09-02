from main import dbert, dbert_token
import numpy as np


# Tests availability of tokenizer
def test_tokenizer(dbert_token=dbert_token):
    sample_string = 'A sample string'
    enc = dbert_token(sample_string)
    assert enc is not None


# Tests sanity of the provided model
def test_model(dbert=dbert, dbert_token=dbert_token):
    true_title = 'Kabul terrorist attack highlights Biden\'s Afghanistan dilemma'
    true_text = "(CNN)America's longest war is ending as it began, with the nation mourning the dead of a terrorist " \
                "attack and an outraged President vowing to hunt down the culprits in Afghanistan. The bloody coda to " \
                "a tortured 20 years -- the loss of 13 US troops and at least 90 Afghans in blasts outside Kabul\'s " \
                "airport on Thursday -- exemplified the human tragedy and ultimate futility of a conflict that failed " \
                "in its core purpose: purging Afghan soil of terrorism. In a cruel irony, the latest Americans to die " \
                "perished in an attack conceived in the very same land as the al Qaeda assault on September 11, 2001, " \
                "that triggered the war they were trying to leave. "
    truth = true_title + ' ' + true_text
    true_embs = dbert_token(truth, padding=True, truncation=True, return_tensors='pt')
    outputs = dbert(**true_embs)
    logits = outputs[0].detach().numpy()
    pred = np.argmax(logits, axis=-1)
    assert pred[0] == 1
    fake_title = 'Godzilla created 9/11 and forced COVID to turn people into zombies!!!'
    fake_text = 'Donald Trump is secretely an alien'
    fake = fake_title + ' ' + fake_text
    fake_embs = dbert_token(fake, padding=True, truncation=True, return_tensors='pt')
    outputs = dbert(**fake_embs)
    logits = outputs[0].detach().numpy()
    pred = np.argmax(logits, axis=-1)
    assert pred[0] == 0
