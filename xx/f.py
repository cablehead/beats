
import vanilla

# TODO: remove
import logging
logging.basicConfig()

ids = [
    'tr10696615',
    'tr99878891',
    'tr4445147',
    'tr35182839',
    'tr3604583',
    'tr101234557',
    'tr922651',
    'tr731867',
    'tr4445161',
    'tr96786793',
    'tr23855583',
    'tr7826301',
    'tr3567729',
    'tr8154791',
    'tr99572115',
    'tr89712007',
    'tr5172283',
    'tr74780459',
    'tr43147375',
    'tr7539093',
    'tr75520197',
    'tr32628957',
    'tr101942991',
    'tr113843941',
    'tr118420749',
    'tr99347151',
    'tr68252107',
    'tr5443531',
    'tr79239223', ]

h = vanilla.Hub()

URI = 'https://partner.api.beatsmusic.com'


collect = h.router()


@h.spawn
def _():
    c = h.http.connect(URI)

    for id in ids:
        while True:
            try:
                r = c.get(
                    '/v1/api/tracks/%s' % id,
                    params={'client_id': 'fxkrj7vemnnxva8jhtqb9wt8'})
                break
            except vanilla.ConnectionLost:
                print "HERE"
                c = h.http.connect(URI)
        collect.send(r)

for r in collect.recver:
    got = r.recv()
    print got
    print got.consume()

