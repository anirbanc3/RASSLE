#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <openssl/obj_mac.h>
#include <openssl/ec.h>
#include <sys/ioctl.h>
#include <asm/unistd.h>
#include <time.h>
#include <linux/perf_event.h>
#include <linux/hw_breakpoint.h>
#include "cacheutils.h"

void ecc_encrypt(char *key)	{
	BN_CTX *ctx = BN_CTX_new();
	BN_CTX_start(ctx);
	
	EC_GROUP *group = EC_GROUP_new_by_curve_name(NID_secp256k1);
	
	
	BIGNUM *k, *order, *x, *y;
	k = BN_CTX_get(ctx);
	order = BN_CTX_get(ctx);
	x = BN_CTX_get(ctx);
	y = BN_CTX_get(ctx);
	
	EC_POINT *P = EC_POINT_new(group);
	EC_POINT *Q = EC_POINT_new(group);

	EC_GROUP_get_order(group, order, ctx);
	
	BN_hex2bn(&k, key);
	
	if (BN_is_zero(k))
		BN_rand_range(k, order);

	
	EC_POINT_mul(group, P, k, NULL, NULL, ctx);

	EC_POINT_make_affine(group, P, ctx);
	
	EC_POINT_get_affine_coordinates_GFp(group, P, x, y, ctx);
	
	char *s0 = BN_bn2hex(k);
	char *s1 = BN_bn2hex(x);
	char *s2 = BN_bn2hex(y);
	
	
	BN_CTX_end(ctx);
	EC_POINT_free(P);
	EC_GROUP_free(group);
	BN_CTX_free(ctx);
	
	free(s0);
	free(s1);
	free(s2);
}


int main(int argc, char* argv[])	{
	CPU_affinity(2);
	int i;
	char key[100];
	strcpy(key, argv[1]);
//	strcat(key, "472D4B6150645367566B59703373367639792442264528482B4D6251655468");

	for (i=0; i< 5; i++)	{
		longnop();
		sched_yield();
	}
	ecc_encrypt(key);
	return 0;
}


