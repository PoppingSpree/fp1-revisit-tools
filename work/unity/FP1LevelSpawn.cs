using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FP1LevelSpawn : MonoBehaviour {

	public Sprite playerstartingpoint_381;
	public GameObject pfCrystal;
	public GameObject pfPetal;
	public static GameObject spawnedLevelContainer;
	public float fp2ScaleFactor = 1.5f;
	public static int drawOrder = 0;
	
	// Why is this a nested class???
	public class BGObjectInfo
	{
		public string name = "";
		public int xpos = 0;
		public int ypos = 0;
		public Sprite sprite = null;
		public bool needsCollider = true;
		public bool isNotBGObject = false;
		public int orderInLayer = 0;
		public GameObject colliderReferenceObject;
	}
	
	public BGObjectInfo create_playerstartingpoint_381(int xpos, int ypos)
	{
		Debug.LogWarning("Using BackgroundObjects to represent an ActiveObject. Fix this.");
		BGObjectInfo obj = new BGObjectInfo();
		obj.name = "playerstartingpoint_381";
		obj.xpos = xpos;
		obj.ypos = ypos;
		obj.sprite = playerstartingpoint_381;
		obj.needsCollider = false;

		try
		{
			var fp2Spawn = GameObject.Find("Player Spawn Point");
			if (fp2Spawn != null)
			{
				fp2Spawn.transform.position = new Vector3(xpos, ypos, 0);
			}
		}
		catch (Exception e)
		{
			Debug.LogError("Failed to find Player Spawn Point: " + e.Message);
		}

		return obj;
	}
	
	public BGObjectInfo create_objectcrystal_316(int xpos, int ypos)
	{
		BGObjectInfo obj = new BGObjectInfo();
		obj.name = "objectcrystal_316";
		obj.xpos = xpos;
		obj.ypos = ypos;
		obj.sprite = null;
		obj.isNotBGObject = true;

		GameObject go = GameObject.Instantiate(pfCrystal);
		SpriteRenderer sr = go.GetComponent<SpriteRenderer>();
		if (sr != null)
		{
			sr.sortingOrder = obj.orderInLayer;	
		}
		go.transform.position = new Vector3(obj.xpos, -obj.ypos, 0);
		go.transform.parent = spawnedLevelContainer.transform;
		return obj;
	}
	
	public BGObjectInfo create_objectpetal_354(int xpos, int ypos)
	{
		BGObjectInfo obj = new BGObjectInfo();
		obj.name = "objectpetal_354";
		obj.xpos = xpos;
		obj.ypos = ypos;
		obj.sprite = null;
		obj.isNotBGObject = true;
		
		GameObject go = GameObject.Instantiate(pfPetal);
		SpriteRenderer sr = go.GetComponent<SpriteRenderer>();
		if (sr != null)
		{
			sr.sortingOrder = obj.orderInLayer;	
		}
		go.transform.position = new Vector3(obj.xpos, -obj.ypos, 0);
		go.transform.parent = spawnedLevelContainer.transform;
		return obj;
	}
	
	/*
	 *add_object(create_objectpetal_354(7505, 289), 2);
    add_object(create_objectcrystal_316(7413, 202), 2);
	 * 
	 */

	public static void add_object(BGObjectInfo obj, int layer)
	{
		Debug.LogWarning("Call to add_object is being handled by add_background_object as a placeholder. Fix this.");
		if (obj.isNotBGObject)
		{
			return;
		}
		else
		{
			obj.isNotBGObject = true;
			obj.needsCollider = true;
		}

		add_background_object(obj, layer);
	}

	public static void add_background_object(BGObjectInfo obj, int layer)
	{
		

		// And now the normal code.

		GameObject go = new GameObject(obj.name);
		SpriteRenderer sr = go.AddComponent<SpriteRenderer>();
		sr.sortingOrder = obj.orderInLayer;
		go.transform.position = new Vector3(obj.xpos, -obj.ypos, 0);
		if (obj.sprite != null)
		{
			sr.sprite = obj.sprite;
			sr.sortingOrder = drawOrder;
			drawOrder--;
			if (obj.needsCollider)
			{
				var col = go.AddComponent<PolygonCollider2D>();
				if (obj.colliderReferenceObject != null) 
				{
					var points = obj.colliderReferenceObject.GetComponent<PolygonCollider2D>().GetPath(0);
					col.SetPath(0, points);
				}
				// Somehow set menuWorldMap.menuWorldMapConfirm.SceneToLoad[currentStageID] = name of this stage.
			}

			if (obj.isNotBGObject)
			{
				go.tag = "Terrain Solid";
				// FG Plane goes ABCD.
				switch (layer)
				{
					case 0:
						go.layer = LayerMask.NameToLayer("FG Plane A");
						break;
					case 1:
						go.layer = LayerMask.NameToLayer("FG Plane B");
						break;
					case 2:
						go.layer = LayerMask.NameToLayer("FG Plane C");
						break;
					case 3:
						go.layer = LayerMask.NameToLayer("FG Plane D");
						break;
					default:
						go.layer = LayerMask.NameToLayer("FG Plane A");
						break;
				}
			}
			else
			{
				// BG Layer goes 0-15.
				// Contrary to the naming implications, 
				// BG Layers are sticky relative to the camera,
				// So most of these should actually be on the FG Layers instead.
				/*
				switch (layer)
				{
					case 0:
						go.layer = LayerMask.NameToLayer("BG Layer 0");
						break;
					case 1:
						go.layer = LayerMask.NameToLayer("BG Layer 1");
						break;
					case 2:
						go.layer = LayerMask.NameToLayer("BG Layer 2");
						break;
					case 3:
						go.layer = LayerMask.NameToLayer("BG Layer 3");
						break;
					case 4:
						go.layer = LayerMask.NameToLayer("BG Layer 4");
						break;
					case 5:
						go.layer = LayerMask.NameToLayer("BG Layer 5");
						break;
					case 6:
						go.layer = LayerMask.NameToLayer("BG Layer 6");
						break;
					case 7:
						go.layer = LayerMask.NameToLayer("BG Layer 7");
						break;
					case 8:
						go.layer = LayerMask.NameToLayer("BG Layer 8");
						break;
					case 9:
						go.layer = LayerMask.NameToLayer("BG Layer 9");
						break;
					case 10:
						go.layer = LayerMask.NameToLayer("BG Layer 10");
						break;
					case 11:
						go.layer = LayerMask.NameToLayer("BG Layer 11");
						break;
					case 12:
						go.layer = LayerMask.NameToLayer("BG Layer 12");
						break;
					case 13:
						go.layer = LayerMask.NameToLayer("BG Layer 13");
						break;
					case 14:
						go.layer = LayerMask.NameToLayer("BG Layer 14");
						break;
					case 15:
						go.layer = LayerMask.NameToLayer("BG Layer 15");
						break;
					default:
						go.layer = LayerMask.NameToLayer("BG Layer 0");
						break;
				}
				*/
				switch (layer)
				{
					case 0:
						go.layer = LayerMask.NameToLayer("FG Plane A");
						break;
					case 1:
						go.layer = LayerMask.NameToLayer("FG Plane B");
						break;
					case 2:
						go.layer = LayerMask.NameToLayer("FG Plane C");
						break;
					case 3:
						go.layer = LayerMask.NameToLayer("FG Plane D");
						break;
					default:
						go.layer = LayerMask.NameToLayer("FG Plane A");
						break;
				}
			}
		}
		else
		{
			// Double check the old source if we should set the Z position by the layer value.
	
			// Get the correct texture by name from the asset library:
			Texture2D tex = (Texture2D)Resources.Load(" " + obj.name);
	
			if (go != null) {
				go.layer = layer;
			}
		}
		
		if (go != null) {
			//go.layer = layer;
			
			// temporarily commented this out, we need to write a function to properly remap 
			// FP1's layers to FP2's layermasks, and they are not the same numbers at all.
			
			go.transform.parent = spawnedLevelContainer.transform;
		}

	
	}
}
