--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6
-- Dumped by pg_dump version 17.0 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.audit_log_entries (instance_id, id, payload, created_at, ip_address) FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.flow_state (id, user_id, auth_code, code_challenge_method, code_challenge, provider_type, provider_access_token, provider_refresh_token, created_at, updated_at, authentication_method, auth_code_issued_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.users (instance_id, id, aud, role, email, encrypted_password, email_confirmed_at, invited_at, confirmation_token, confirmation_sent_at, recovery_token, recovery_sent_at, email_change_token_new, email_change, email_change_sent_at, last_sign_in_at, raw_app_meta_data, raw_user_meta_data, is_super_admin, created_at, updated_at, phone, phone_confirmed_at, phone_change, phone_change_token, phone_change_sent_at, email_change_token_current, email_change_confirm_status, banned_until, reauthentication_token, reauthentication_sent_at, is_sso_user, deleted_at, is_anonymous) FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.identities (provider_id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at, id) FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.instances (id, uuid, raw_base_config, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sessions (id, user_id, created_at, updated_at, factor_id, aal, not_after, refreshed_at, user_agent, ip, tag) FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_amr_claims (session_id, created_at, updated_at, authentication_method, id) FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_factors (id, user_id, friendly_name, factor_type, status, created_at, updated_at, secret, phone, last_challenged_at, web_authn_credential, web_authn_aaguid) FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_challenges (id, factor_id, created_at, verified_at, ip_address, otp_code, web_authn_session_data) FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.one_time_tokens (id, user_id, token_type, token_hash, relates_to, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.refresh_tokens (instance_id, id, token, user_id, revoked, created_at, updated_at, parent, session_id) FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sso_providers (id, resource_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.saml_providers (id, sso_provider_id, entity_id, metadata_xml, metadata_url, attribute_mapping, created_at, updated_at, name_id_format) FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.saml_relay_states (id, sso_provider_id, request_id, for_email, redirect_to, created_at, updated_at, flow_state_id) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.schema_migrations (version) FROM stdin;
20171026211738
20171026211808
20171026211834
20180103212743
20180108183307
20180119214651
20180125194653
00
20210710035447
20210722035447
20210730183235
20210909172000
20210927181326
20211122151130
20211124214934
20211202183645
20220114185221
20220114185340
20220224000811
20220323170000
20220429102000
20220531120530
20220614074223
20220811173540
20221003041349
20221003041400
20221011041400
20221020193600
20221021073300
20221021082433
20221027105023
20221114143122
20221114143410
20221125140132
20221208132122
20221215195500
20221215195800
20221215195900
20230116124310
20230116124412
20230131181311
20230322519590
20230402418590
20230411005111
20230508135423
20230523124323
20230818113222
20230914180801
20231027141322
20231114161723
20231117164230
20240115144230
20240214120130
20240306115329
20240314092811
20240427152123
20240612123726
20240729123726
20240802193726
20240806073726
20241009103726
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sso_domains (id, sso_provider_id, domain, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: job; Type: TABLE DATA; Schema: cron; Owner: supabase_admin
--

COPY cron.job (jobid, schedule, command, nodename, nodeport, database, username, active, jobname) FROM stdin;
2	*/10 * * * *	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	localhost	5432	postgres	postgres	t	keeping chore tracker alive
\.


--
-- Data for Name: job_run_details; Type: TABLE DATA; Schema: cron; Owner: supabase_admin
--

COPY cron.job_run_details (jobid, runid, job_pid, database, username, command, status, return_message, start_time, end_time) FROM stdin;
2	22	701284	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 01:40:00.015493+00	2024-12-01 01:40:00.01852+00
2	8	699364	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 23:20:00.017879+00	2024-11-30 23:20:00.021545+00
2	14	700172	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 00:20:00.016597+00	2024-12-01 00:20:00.019797+00
3	2	698529	postgres	postgres	\n    select\n      net.http_post(\n          url:='https://chore-tracker-api.onrender.com/?ping=true',\n          headers:=jsonb_build_object(),\n          body:='',\n          timeout_milliseconds:=1000\n      );\n    	failed	ERROR:  invalid input syntax for type json\nLINE 6:           body:='',\n                        ^\nDETAIL:  The input string ended unexpectedly.\nCONTEXT:  JSON data, line 1: \n	2024-11-30 22:20:00.073157+00	2024-11-30 22:20:00.074533+00
2	1	698528	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 22:20:00.071718+00	2024-11-30 22:20:00.083191+00
2	19	700874	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 01:10:00.016813+00	2024-12-01 01:10:00.019831+00
2	9	699493	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 23:30:00.016548+00	2024-11-30 23:30:00.019542+00
2	3	698697	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 22:30:00.015547+00	2024-11-30 22:30:00.019479+00
2	4	698842	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 22:40:00.016606+00	2024-11-30 22:40:00.019524+00
2	15	700302	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 00:30:00.020257+00	2024-12-01 00:30:00.023358+00
2	10	699621	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 23:40:00.018736+00	2024-11-30 23:40:00.021787+00
2	5	698973	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 22:50:00.016348+00	2024-11-30 22:50:00.019524+00
2	23	701425	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 01:50:00.016041+00	2024-12-01 01:50:00.019612+00
2	6	699101	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 23:00:00.016869+00	2024-11-30 23:00:00.019903+00
2	11	699769	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 23:50:00.015768+00	2024-11-30 23:50:00.018842+00
2	20	701006	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 01:20:00.015841+00	2024-12-01 01:20:00.019021+00
2	7	699233	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-11-30 23:10:00.016619+00	2024-11-30 23:10:00.019634+00
2	16	700431	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 00:40:00.016308+00	2024-12-01 00:40:00.019278+00
2	12	699901	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 00:00:00.018085+00	2024-12-01 00:00:00.021143+00
2	13	700041	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 00:10:00.019718+00	2024-12-01 00:10:00.024069+00
2	17	700591	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 00:50:00.017797+00	2024-12-01 00:50:00.020858+00
2	21	701153	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 01:30:00.023187+00	2024-12-01 01:30:00.027599+00
2	18	700741	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 01:00:00.017027+00	2024-12-01 01:00:00.020164+00
2	24	701596	postgres	postgres	 SELECT\n  net.http_get (\n    url := 'https://chore-tracker-api.onrender.com/?ping=true'\n  );\n	succeeded	1 row	2024-12-01 02:00:00.018794+00	2024-12-01 02:00:00.0226+00
\.


--
-- Data for Name: key; Type: TABLE DATA; Schema: pgsodium; Owner: supabase_admin
--

COPY pgsodium.key (id, status, created, expires, key_type, key_id, key_context, name, associated_data, raw_key, raw_key_nonce, parent_key, comment, user_data) FROM stdin;
\.


--
-- Data for Name: bill; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bill (id, cost, due_date, bill_type, message) FROM stdin;
47	40.57	2024-11-19	electricity	string
48	40.57	2024-11-19	electricity	string
42	40.57	2024-11-19	electricity	string
46	40.57	2024-11-19	electricity	string
\.


--
-- Data for Name: bill_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bill_list (id, bill_id, roommate_id, status, amount) FROM stdin;
307	47	1	unpaid	8.11
308	47	2	unpaid	8.11
309	47	3	unpaid	8.11
310	47	4	unpaid	8.12
311	47	23	unpaid	8.12
312	48	1	unpaid	10.14
313	48	2	unpaid	10.14
314	48	3	unpaid	10.14
315	48	4	unpaid	10.15
\.


--
-- Data for Name: chore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chore (id, name, location_in_house, frequency, duration_mins, priority, due_date) FROM stdin;
1	mop floors	All rooms	weekly	25	5	2024-10-27
9	Clean the bathroom	bathroom	weekly	20	5	2024-11-09
14	Deep clean kitchen	kitchen	weekly	45	5	2024-11-16
28	Clean	Bedroom	daily	60	5	2024-11-11
5	clean your room	bedroom	weekly	30	5	2024-11-05
46	string	string	daily	0	1	2024-11-28
\.


--
-- Data for Name: roommate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roommate (id, first_name, last_name, email) FROM stdin;
1	Antony	LeGoat	bigballer@gmail.com
2	sue	sue	test@gmail.com
3	Billy	Bob	billybob@gmail.com
4	Lisa	Olander	lo@gmail.com
\.


--
-- Data for Name: chore_assignment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chore_assignment (id, chore_id, roommate_id, status) FROM stdin;
29	5	2	pending
30	9	3	pending
28	1	2	pending
31	14	1	pending
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--

COPY realtime.schema_migrations (version, inserted_at) FROM stdin;
20211116024918	2024-10-27 03:45:41
20211116045059	2024-10-27 03:45:41
20211116050929	2024-10-27 03:45:41
20211116051442	2024-10-27 03:45:41
20211116212300	2024-10-27 03:45:41
20211116213355	2024-10-27 03:45:41
20211116213934	2024-10-27 03:45:41
20211116214523	2024-10-27 03:45:41
20211122062447	2024-10-27 03:45:41
20211124070109	2024-10-27 03:45:41
20211202204204	2024-10-27 03:45:41
20211202204605	2024-10-27 03:45:41
20211210212804	2024-10-27 03:45:41
20211228014915	2024-10-27 03:45:41
20220107221237	2024-10-27 03:45:41
20220228202821	2024-10-27 03:45:41
20220312004840	2024-10-27 03:45:41
20220603231003	2024-10-27 03:45:41
20220603232444	2024-10-27 03:45:41
20220615214548	2024-10-27 03:45:41
20220712093339	2024-10-27 03:45:41
20220908172859	2024-10-27 03:45:41
20220916233421	2024-10-27 03:45:41
20230119133233	2024-10-27 03:45:41
20230128025114	2024-10-27 03:45:41
20230128025212	2024-10-27 03:45:41
20230227211149	2024-10-27 03:45:41
20230228184745	2024-10-27 03:45:41
20230308225145	2024-10-27 03:45:41
20230328144023	2024-10-27 03:45:41
20231018144023	2024-10-27 03:45:41
20231204144023	2024-10-27 03:45:41
20231204144024	2024-10-27 03:45:41
20231204144025	2024-10-27 03:45:41
20240108234812	2024-10-27 03:45:41
20240109165339	2024-10-27 03:45:41
20240227174441	2024-10-27 03:45:41
20240311171622	2024-10-27 03:45:41
20240321100241	2024-10-27 03:45:41
20240401105812	2024-10-27 03:45:41
20240418121054	2024-10-27 03:45:41
20240523004032	2024-10-27 03:45:41
20240618124746	2024-10-27 03:45:41
20240801235015	2024-10-27 03:45:41
20240805133720	2024-10-27 03:45:41
20240827160934	2024-10-27 03:45:41
20240919163303	2024-11-19 03:28:13
20240919163305	2024-11-19 03:28:13
20241019105805	2024-11-19 03:28:13
20241030150047	2024-11-19 03:28:13
20241108114728	2024-11-19 03:28:13
20241121104152	2024-11-28 16:52:40
\.


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--

COPY realtime.subscription (id, subscription_id, entity, filters, claims, created_at) FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets (id, name, owner, created_at, updated_at, public, avif_autodetection, file_size_limit, allowed_mime_types, owner_id) FROM stdin;
\.


--
-- Data for Name: migrations; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.migrations (id, name, hash, executed_at) FROM stdin;
0	create-migrations-table	e18db593bcde2aca2a408c4d1100f6abba2195df	2024-10-27 03:42:52.935996
1	initialmigration	6ab16121fbaa08bbd11b712d05f358f9b555d777	2024-10-27 03:42:52.953635
2	storage-schema	5c7968fd083fcea04050c1b7f6253c9771b99011	2024-10-27 03:42:53.001901
3	pathtoken-column	2cb1b0004b817b29d5b0a971af16bafeede4b70d	2024-10-27 03:42:53.079535
4	add-migrations-rls	427c5b63fe1c5937495d9c635c263ee7a5905058	2024-10-27 03:42:53.159562
5	add-size-functions	79e081a1455b63666c1294a440f8ad4b1e6a7f84	2024-10-27 03:42:53.168665
6	change-column-name-in-get-size	f93f62afdf6613ee5e7e815b30d02dc990201044	2024-10-27 03:42:53.218743
7	add-rls-to-buckets	e7e7f86adbc51049f341dfe8d30256c1abca17aa	2024-10-27 03:42:53.226701
8	add-public-to-buckets	fd670db39ed65f9d08b01db09d6202503ca2bab3	2024-10-27 03:42:53.279026
9	fix-search-function	3a0af29f42e35a4d101c259ed955b67e1bee6825	2024-10-27 03:42:53.286337
10	search-files-search-function	68dc14822daad0ffac3746a502234f486182ef6e	2024-10-27 03:42:52.88715
11	add-trigger-to-auto-update-updated_at-column	7425bdb14366d1739fa8a18c83100636d74dcaa2	2024-10-27 03:42:52.895606
12	add-automatic-avif-detection-flag	8e92e1266eb29518b6a4c5313ab8f29dd0d08df9	2024-10-27 03:42:52.953837
13	add-bucket-custom-limits	cce962054138135cd9a8c4bcd531598684b25e7d	2024-10-27 03:42:52.962047
14	use-bytes-for-max-size	941c41b346f9802b411f06f30e972ad4744dad27	2024-10-27 03:42:52.969845
15	add-can-insert-object-function	934146bc38ead475f4ef4b555c524ee5d66799e5	2024-10-27 03:42:53.039078
16	add-version	76debf38d3fd07dcfc747ca49096457d95b1221b	2024-10-27 03:42:53.089571
17	drop-owner-foreign-key	f1cbb288f1b7a4c1eb8c38504b80ae2a0153d101	2024-10-27 03:42:53.143296
18	add_owner_id_column_deprecate_owner	e7a511b379110b08e2f214be852c35414749fe66	2024-10-27 03:42:53.200457
19	alter-default-value-objects-id	02e5e22a78626187e00d173dc45f58fa66a4f043	2024-10-27 03:42:53.252911
20	list-objects-with-delimiter	cd694ae708e51ba82bf012bba00caf4f3b6393b7	2024-10-27 03:42:53.304679
21	s3-multipart-uploads	8c804d4a566c40cd1e4cc5b3725a664a9303657f	2024-10-27 03:42:53.374063
22	s3-multipart-uploads-big-ints	9737dc258d2397953c9953d9b86920b8be0cdb73	2024-10-27 03:42:53.449443
23	optimize-search-function	9d7e604cddc4b56a5422dc68c9313f4a1b6f132c	2024-10-27 03:42:53.517625
24	operation-function	8312e37c2bf9e76bbe841aa5fda889206d2bf8aa	2024-10-27 03:42:53.569121
25	custom-metadata	67eb93b7e8d401cafcdc97f9ac779e71a79bfe03	2024-10-27 03:42:53.621196
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.objects (id, bucket_id, name, owner, created_at, updated_at, last_accessed_at, metadata, version, owner_id, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.s3_multipart_uploads (id, in_progress_size, upload_signature, bucket_id, key, version, owner_id, created_at, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.s3_multipart_uploads_parts (id, upload_id, size, part_number, bucket_id, key, etag, owner_id, version, created_at) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: supabase_migrations; Owner: postgres
--

COPY supabase_migrations.schema_migrations (version, statements, name) FROM stdin;
20241130054746	{"SET statement_timeout = 0","SET lock_timeout = 0","SET idle_in_transaction_session_timeout = 0","SET client_encoding = 'UTF8'","SET standard_conforming_strings = on","SELECT pg_catalog.set_config('search_path', '', false)","SET check_function_bodies = false","SET xmloption = content","SET client_min_messages = warning","SET row_security = off","CREATE EXTENSION IF NOT EXISTS \\"pg_cron\\" WITH SCHEMA \\"pg_catalog\\"","CREATE EXTENSION IF NOT EXISTS \\"pgsodium\\" WITH SCHEMA \\"pgsodium\\"","COMMENT ON SCHEMA \\"public\\" IS 'standard public schema'","CREATE EXTENSION IF NOT EXISTS \\"pg_graphql\\" WITH SCHEMA \\"graphql\\"","CREATE EXTENSION IF NOT EXISTS \\"pg_stat_statements\\" WITH SCHEMA \\"extensions\\"","CREATE EXTENSION IF NOT EXISTS \\"pgcrypto\\" WITH SCHEMA \\"extensions\\"","CREATE EXTENSION IF NOT EXISTS \\"pgjwt\\" WITH SCHEMA \\"extensions\\"","CREATE EXTENSION IF NOT EXISTS \\"supabase_vault\\" WITH SCHEMA \\"vault\\"","CREATE EXTENSION IF NOT EXISTS \\"uuid-ossp\\" WITH SCHEMA \\"extensions\\"","CREATE TYPE \\"public\\".\\"bill_type_enum\\" AS ENUM (\n    'electricity',\n    'water',\n    'internet',\n    'rent',\n    'gas',\n    'trash',\n    'groceries'\n)","ALTER TYPE \\"public\\".\\"bill_type_enum\\" OWNER TO \\"postgres\\"","CREATE TYPE \\"public\\".\\"frequency_enum\\" AS ENUM (\n    'daily',\n    'weekly',\n    'biweekly',\n    'monthly',\n    'bimonthly',\n    'yearly'\n)","ALTER TYPE \\"public\\".\\"frequency_enum\\" OWNER TO \\"postgres\\"","CREATE TYPE \\"public\\".\\"status_enum\\" AS ENUM (\n    'unpaid',\n    'paid',\n    'overdue'\n)","ALTER TYPE \\"public\\".\\"status_enum\\" OWNER TO \\"postgres\\"","CREATE TYPE \\"public\\".\\"status_type\\" AS ENUM (\n    'pending',\n    'in_progress',\n    'completed'\n)","ALTER TYPE \\"public\\".\\"status_type\\" OWNER TO \\"postgres\\"","SET default_tablespace = ''","SET default_table_access_method = \\"heap\\"","CREATE TABLE IF NOT EXISTS \\"public\\".\\"bill\\" (\n    \\"id\\" bigint NOT NULL,\n    \\"cost\\" double precision,\n    \\"due_date\\" \\"date\\",\n    \\"bill_type\\" \\"public\\".\\"bill_type_enum\\",\n    \\"message\\" \\"text\\"\n)","ALTER TABLE \\"public\\".\\"bill\\" OWNER TO \\"postgres\\"","ALTER TABLE \\"public\\".\\"bill\\" ALTER COLUMN \\"id\\" ADD GENERATED BY DEFAULT AS IDENTITY (\n    SEQUENCE NAME \\"public\\".\\"bill_id_seq\\"\n    START WITH 1\n    INCREMENT BY 1\n    NO MINVALUE\n    NO MAXVALUE\n    CACHE 1\n)","CREATE TABLE IF NOT EXISTS \\"public\\".\\"bill_list\\" (\n    \\"id\\" bigint NOT NULL,\n    \\"bill_id\\" bigint,\n    \\"roommate_id\\" bigint,\n    \\"status\\" \\"public\\".\\"status_enum\\",\n    \\"amount\\" real DEFAULT '0'::real NOT NULL\n)","ALTER TABLE \\"public\\".\\"bill_list\\" OWNER TO \\"postgres\\"","ALTER TABLE \\"public\\".\\"bill_list\\" ALTER COLUMN \\"id\\" ADD GENERATED BY DEFAULT AS IDENTITY (\n    SEQUENCE NAME \\"public\\".\\"bill_list_id_seq\\"\n    START WITH 1\n    INCREMENT BY 1\n    NO MINVALUE\n    NO MAXVALUE\n    CACHE 1\n)","CREATE TABLE IF NOT EXISTS \\"public\\".\\"chore\\" (\n    \\"id\\" bigint NOT NULL,\n    \\"name\\" \\"text\\",\n    \\"location_in_house\\" \\"text\\",\n    \\"frequency\\" \\"public\\".\\"frequency_enum\\",\n    \\"duration_mins\\" bigint DEFAULT '0'::bigint,\n    \\"priority\\" integer,\n    \\"due_date\\" \\"date\\",\n    CONSTRAINT \\"chore_priority_check\\" CHECK (((\\"priority\\" >= 1) AND (\\"priority\\" <= 5)))\n)","ALTER TABLE \\"public\\".\\"chore\\" OWNER TO \\"postgres\\"","CREATE TABLE IF NOT EXISTS \\"public\\".\\"chore_assignment\\" (\n    \\"id\\" bigint NOT NULL,\n    \\"chore_id\\" bigint,\n    \\"roommate_id\\" bigint,\n    \\"status\\" \\"text\\",\n    CONSTRAINT \\"status_check\\" CHECK ((\\"status\\" = ANY (ARRAY['pending'::\\"text\\", 'in_progress'::\\"text\\", 'completed'::\\"text\\"])))\n)","ALTER TABLE \\"public\\".\\"chore_assignment\\" OWNER TO \\"postgres\\"","ALTER TABLE \\"public\\".\\"chore_assignment\\" ALTER COLUMN \\"id\\" ADD GENERATED BY DEFAULT AS IDENTITY (\n    SEQUENCE NAME \\"public\\".\\"chore_assignment_id_seq\\"\n    START WITH 1\n    INCREMENT BY 1\n    NO MINVALUE\n    NO MAXVALUE\n    CACHE 1\n)","ALTER TABLE \\"public\\".\\"chore\\" ALTER COLUMN \\"id\\" ADD GENERATED BY DEFAULT AS IDENTITY (\n    SEQUENCE NAME \\"public\\".\\"chore_id_seq\\"\n    START WITH 1\n    INCREMENT BY 1\n    NO MINVALUE\n    NO MAXVALUE\n    CACHE 1\n)","CREATE TABLE IF NOT EXISTS \\"public\\".\\"roommate\\" (\n    \\"id\\" bigint NOT NULL,\n    \\"first_name\\" \\"text\\",\n    \\"last_name\\" \\"text\\",\n    \\"email\\" \\"text\\"\n)","ALTER TABLE \\"public\\".\\"roommate\\" OWNER TO \\"postgres\\"","ALTER TABLE \\"public\\".\\"roommate\\" ALTER COLUMN \\"id\\" ADD GENERATED BY DEFAULT AS IDENTITY (\n    SEQUENCE NAME \\"public\\".\\"roommate_id_seq\\"\n    START WITH 1\n    INCREMENT BY 1\n    NO MINVALUE\n    NO MAXVALUE\n    CACHE 1\n)","ALTER TABLE ONLY \\"public\\".\\"bill_list\\"\n    ADD CONSTRAINT \\"bill_list_pkey\\" PRIMARY KEY (\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"bill\\"\n    ADD CONSTRAINT \\"bill_pkey\\" PRIMARY KEY (\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"chore_assignment\\"\n    ADD CONSTRAINT \\"chore_assignment_pkey\\" PRIMARY KEY (\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"chore\\"\n    ADD CONSTRAINT \\"chore_pkey\\" PRIMARY KEY (\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"roommate\\"\n    ADD CONSTRAINT \\"roommate_pkey\\" PRIMARY KEY (\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"bill_list\\"\n    ADD CONSTRAINT \\"bill_list_bill_id_fkey\\" FOREIGN KEY (\\"bill_id\\") REFERENCES \\"public\\".\\"bill\\"(\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"chore_assignment\\"\n    ADD CONSTRAINT \\"chore_assignment_chore_id_fkey\\" FOREIGN KEY (\\"chore_id\\") REFERENCES \\"public\\".\\"chore\\"(\\"id\\")","ALTER TABLE ONLY \\"public\\".\\"chore_assignment\\"\n    ADD CONSTRAINT \\"chore_assignment_roommate_id_fkey\\" FOREIGN KEY (\\"roommate_id\\") REFERENCES \\"public\\".\\"roommate\\"(\\"id\\")","ALTER TABLE \\"public\\".\\"bill\\" ENABLE ROW LEVEL SECURITY","ALTER TABLE \\"public\\".\\"bill_list\\" ENABLE ROW LEVEL SECURITY","ALTER TABLE \\"public\\".\\"chore\\" ENABLE ROW LEVEL SECURITY","ALTER TABLE \\"public\\".\\"chore_assignment\\" ENABLE ROW LEVEL SECURITY","ALTER TABLE \\"public\\".\\"roommate\\" ENABLE ROW LEVEL SECURITY","ALTER PUBLICATION \\"supabase_realtime\\" OWNER TO \\"postgres\\"","GRANT USAGE ON SCHEMA \\"public\\" TO \\"postgres\\"","GRANT USAGE ON SCHEMA \\"public\\" TO \\"anon\\"","GRANT USAGE ON SCHEMA \\"public\\" TO \\"authenticated\\"","GRANT USAGE ON SCHEMA \\"public\\" TO \\"service_role\\"","GRANT ALL ON TABLE \\"public\\".\\"bill\\" TO \\"anon\\"","GRANT ALL ON TABLE \\"public\\".\\"bill\\" TO \\"authenticated\\"","GRANT ALL ON TABLE \\"public\\".\\"bill\\" TO \\"service_role\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"bill_id_seq\\" TO \\"anon\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"bill_id_seq\\" TO \\"authenticated\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"bill_id_seq\\" TO \\"service_role\\"","GRANT ALL ON TABLE \\"public\\".\\"bill_list\\" TO \\"anon\\"","GRANT ALL ON TABLE \\"public\\".\\"bill_list\\" TO \\"authenticated\\"","GRANT ALL ON TABLE \\"public\\".\\"bill_list\\" TO \\"service_role\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"bill_list_id_seq\\" TO \\"anon\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"bill_list_id_seq\\" TO \\"authenticated\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"bill_list_id_seq\\" TO \\"service_role\\"","GRANT ALL ON TABLE \\"public\\".\\"chore\\" TO \\"anon\\"","GRANT ALL ON TABLE \\"public\\".\\"chore\\" TO \\"authenticated\\"","GRANT ALL ON TABLE \\"public\\".\\"chore\\" TO \\"service_role\\"","GRANT ALL ON TABLE \\"public\\".\\"chore_assignment\\" TO \\"anon\\"","GRANT ALL ON TABLE \\"public\\".\\"chore_assignment\\" TO \\"authenticated\\"","GRANT ALL ON TABLE \\"public\\".\\"chore_assignment\\" TO \\"service_role\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"chore_assignment_id_seq\\" TO \\"anon\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"chore_assignment_id_seq\\" TO \\"authenticated\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"chore_assignment_id_seq\\" TO \\"service_role\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"chore_id_seq\\" TO \\"anon\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"chore_id_seq\\" TO \\"authenticated\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"chore_id_seq\\" TO \\"service_role\\"","GRANT ALL ON TABLE \\"public\\".\\"roommate\\" TO \\"anon\\"","GRANT ALL ON TABLE \\"public\\".\\"roommate\\" TO \\"authenticated\\"","GRANT ALL ON TABLE \\"public\\".\\"roommate\\" TO \\"service_role\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"roommate_id_seq\\" TO \\"anon\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"roommate_id_seq\\" TO \\"authenticated\\"","GRANT ALL ON SEQUENCE \\"public\\".\\"roommate_id_seq\\" TO \\"service_role\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON SEQUENCES  TO \\"postgres\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON SEQUENCES  TO \\"anon\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON SEQUENCES  TO \\"authenticated\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON SEQUENCES  TO \\"service_role\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON FUNCTIONS  TO \\"postgres\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON FUNCTIONS  TO \\"anon\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON FUNCTIONS  TO \\"authenticated\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON FUNCTIONS  TO \\"service_role\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON TABLES  TO \\"postgres\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON TABLES  TO \\"anon\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON TABLES  TO \\"authenticated\\"","ALTER DEFAULT PRIVILEGES FOR ROLE \\"postgres\\" IN SCHEMA \\"public\\" GRANT ALL ON TABLES  TO \\"service_role\\"","RESET ALL"}	remote_schema
\.


--
-- Data for Name: seed_files; Type: TABLE DATA; Schema: supabase_migrations; Owner: postgres
--

COPY supabase_migrations.seed_files (path, hash) FROM stdin;
\.


--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--

COPY vault.secrets (id, name, description, secret, key_id, nonce, created_at, updated_at) FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('auth.refresh_tokens_id_seq', 1, false);


--
-- Name: jobid_seq; Type: SEQUENCE SET; Schema: cron; Owner: supabase_admin
--

SELECT pg_catalog.setval('cron.jobid_seq', 3, true);


--
-- Name: runid_seq; Type: SEQUENCE SET; Schema: cron; Owner: supabase_admin
--

SELECT pg_catalog.setval('cron.runid_seq', 24, true);


--
-- Name: key_key_id_seq; Type: SEQUENCE SET; Schema: pgsodium; Owner: supabase_admin
--

SELECT pg_catalog.setval('pgsodium.key_key_id_seq', 1, false);


--
-- Name: bill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bill_id_seq', 48, true);


--
-- Name: bill_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bill_list_id_seq', 315, true);


--
-- Name: chore_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chore_assignment_id_seq', 31, true);


--
-- Name: chore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chore_id_seq', 46, true);


--
-- Name: roommate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roommate_id_seq', 29, true);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: realtime; Owner: supabase_admin
--

SELECT pg_catalog.setval('realtime.subscription_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

