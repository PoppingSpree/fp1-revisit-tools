using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FP1LevelSpawn : MonoBehaviour {

	public Sprite playerstartingpoint_381;
	public GameObject pfCrystal;
	public GameObject pfPetal;
	private static GameObject spawnedLevelContainer;
	private float fp2ScaleFactor = 1.5f;
	
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

		add_background_object(obj, layer);
	}

	public static void add_background_object(BGObjectInfo obj, int layer)
	{
		GameObject go = new GameObject(obj.name);
		SpriteRenderer sr = go.AddComponent<SpriteRenderer>();
		sr.sortingOrder = obj.orderInLayer;
		go.transform.position = new Vector3(obj.xpos, -obj.ypos, 0);
		if (obj.sprite != null)
		{
			sr.sprite = obj.sprite;
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

			go.layer = LayerMask.NameToLayer("FG Plane A");
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
