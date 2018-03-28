from tantalus.backend.scripts.utils import *
from tantalus.backend.gsc_queries import query_gsc_wgs_bams
from tantalus.models import GscWgsBamQuery


if __name__ == '__main__':
    args = utils.parse_args()
    utils.run_task(args['primary_key'], GscWgsBamQuery, query_gsc_wgs_bams)